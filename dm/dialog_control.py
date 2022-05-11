from dm.context_model import DialogContextModel, Intent
from db.potion_dictionary import potions, ingredients
from generation.response_generation import *


class DialogControl:

    def __init__(self, dialog_context_model: DialogContextModel) -> None:
        super().__init__()
        self._dialog_context_model = dialog_context_model
        self._response_generator = ResponseGenerator()
        self._n_questions = random.randrange(5, 10)

    def choose_output(self):
        mem = self._dialog_context_model.memory.get_data_frame()
        potion = self._dialog_context_model.context.name

        if mem.empty:  # la prima interazione è HANDSHAKE --> memoria vuota
            self._dialog_context_model.memory.system_update(intent=Intent.HANDSHAKE)
            return self._response_generator.greeting(self._dialog_context_model.context.name)
        else:
            right = mem['right'].values[-1]
            wrong = mem['wrong'].values[-1]
            complete = mem['complete'].values[-1]
            intent = mem['intent'].values[-1]
            sentence = mem['sentence'].values[-1]
            expected = mem['expected'].values[-1]
            end_eval_matches = mem['matched'].values[-1] is False and (
                    mem['matched'].values[-1] and mem['matched'].values[-2] and mem['matched'].values[-3])
            self._n_questions -= 1

            ingredient = None
            if intent == Intent.HANDSHAKE:  # la seconda interazione chiede gli ingredienti della pozione asociata al frame --> tutti gli ingredienti sono in 'expected'
                self._dialog_context_model.memory.system_update(intent=Intent.INGREDIENTS, expected=potions[potion])
                return self._response_generator.initiate_exam(potion)
            else:  # entro qui a partire dalla terza volta che Piton parla
                if sentence != sentence:
                    return self._response_generator.back_up_strategy()
                elif intent == Intent.INGREDIENTS and len(right) == 0 and len(wrong) == 0:
                    self._dialog_context_model.memory.system_update(intent=intent, expected=expected)
                    return self._response_generator.refusal()
                elif complete == 100 or self._n_questions < 0 or end_eval_matches:  # il frame è stato completato --> passo alla valutazione
                    self._dialog_context_model.memory.system_update(intent=Intent.EVALUATION)
                    return self._response_generator.eval(complete, self._n_questions, end_eval_matches,
                                                         mem['matched'].values)
                else:
                    i = None
                    if intent == Intent.INGREDIENTS:
                        i = [Intent.INGREDIENTS, Intent.Y_N_INGREDIENT, Intent.Y_N][
                            random.randrange(3)]  # genero un intent casualmente
                    elif intent == Intent.Y_N or intent == Intent.Y_N_INGREDIENT:
                        i = [Intent.INGREDIENTS, Intent.Y_N_INGREDIENT][
                            random.randrange(2)]

                    if i == Intent.INGREDIENTS:  # richiedo gli ingredienti --> in 'expected' ci sono gli ingredienti della pozione mancanti dal frame
                        expected = [ing for ing in potions[potion] if
                                    ing not in self._dialog_context_model.context.get_ingredients()]
                    elif i == Intent.Y_N_INGREDIENT:  # scelgo un ingrediente a caso dalla lista degli ingredienti (escludendo quelli già elencati e nel frame) --> in 'expected' Yes/No
                        ings = [i for i in ingredients if i not in self._dialog_context_model.context.get_ingredients()]
                        ingredient = ings[random.randrange(len(ings))]
                        expected = [ingredient in potions[potion], ingredient]
                    else:  # domanda del tipo Yes/No --> setto casualmente 'expected' e genererò la domanda in base a questo in clarif
                        if len(wrong) > 0:
                            expected = 'no'
                            ingredient = wrong[random.randrange(len(wrong))]
                        else:
                            expected = 'yes'
                            ingredient = right[random.randrange(len(right))]

                    self._dialog_context_model.memory.system_update(intent=i, expected=expected)
                    return self._response_generator.clarify(mem, ingredient=ingredient)
