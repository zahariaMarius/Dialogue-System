from dm.context_model import DialogContextModel, Intent
from db.potion_dictionary import potions, ingredients
from generation.response_generation import *


class DialogControl:

    def __init__(self, dialog_context_model: DialogContextModel) -> None:
        super().__init__()
        self._dialog_context_model = dialog_context_model
        self._response_generator = ResponseGenerator()

    def choose_output(self):
        mem = self._dialog_context_model.memory.get_data_frame()
        potion = self._dialog_context_model.context.name
        print(mem.size)
        if mem.empty:                                                                                #la prima interazione è HANDSHAKE --> memoria vuota
            self._dialog_context_model.memory.system_update(intent=Intent.HANDSHAKE)
            return self._response_generator.greeting(self._dialog_context_model.context.name)
        else:
            if mem['intent'][mem.index[-1]] == Intent.HANDSHAKE:                                      #la seconda interazione chiede gli ingredienti della pozione asociata al frame --> tutti gli ingredienti sono in 'expected'
                self._dialog_context_model.memory.system_update(intent=Intent.INGREDIENTS, expected=potions[potion])
                return self._response_generator.initiate_exam(potion)
            else:                                                                                    #entro qui a partire dalla terza volta che Piton parla
                right = mem['right'].values[-1]
                wrong = mem['wrong'].values[-1]
                complete = mem['complete'].values[-1]
                if right == 0 and wrong == 0:                                                         #non sono stati detti né ingredienti giusti né sbagliati --> richiedo gli ingredienti
                    self._dialog_context_model.memory.system_update(intent=Intent.INGREDIENTS)  # aggiungere expected
                    return self._response_generator.refusal()
                elif complete == 100:                                                                 # il frame è stato completato --> passo alla valutazione
                    self._dialog_context_model.memory.set_intent('evaluation')
                    return self._response_generator.approval()
                else:
                    i = [Intent.INGREDIENTS, Intent.Y_N_INGREDIENT, Intent.Y_N][random.randrange(3)]  #genero un intent casualmente
                    if i == Intent.INGREDIENTS:                                                       #richiedo gli ingredienti --> in 'expected' ci sono gli ingredienti della pozione mancanti dal frame
                        expected = [ing for ing in potions[potion] if
                                    ing not in self._dialog_context_model.context.get_ingredients()]
                    elif i == Intent.Y_N_INGREDIENT:                                                  #scelgo un ingrediente a caso dalla lista degli ingredienti (escludendo quelli già elencati e nel frame) --> in 'expected' Yes/No
                        ings = [i for i in ingredients if i not in self._dialog_context_model.context.get_ingredients()]
                        ingredient = ings[random.randrange(len(ings))]
                        expected = [ingredient in potions[potion], ingredient]
                    else:                                                                               # domanda del tipo Yes/No --> setto casualmente 'expected' e genererò la domanda in base a questo in clarify
                        expected = ['yes', 'no'][random.randrange(2)]
                    self._dialog_context_model.memory.system_update(intent=i, expected=expected)
                    return self._response_generator.clarify(mem, expected)
