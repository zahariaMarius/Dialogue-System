import random
from db.potion_dictionary import potions, ingredients, pos_words, neg_words
from dm import frames
from analysis import language_understanding as lu
import pandas as pd
from enum import Enum


class Intent(Enum):
    HANDSHAKE = 0
    N_INGREDIENTS = 1
    INGREDIENTS = 2
    Y_N = 3
    Y_N_INGREDIENT = 4
    EVALUATION = 5



"""
Classe che gestisce la memoria, è una tabella con i seguenti campi:
- intent --> l'intent del sistema (tipo di domanda)
- expected --> la giusta risposta che il sistema si aspetta di ricevere
- sentence --> la risposta dell'utente al sistema
- right --> numero di ingredienti giusti all'interno della sentence
- wrong --> nuemero di ingredienti sbagliati all'interno della sentence
- matched --> True se la sentence == expected, False altrimenti
- complete --> numero di slot del frame riepiti 
"""


class Memory:

    def __init__(self) -> None:
        super().__init__()
        self._data_frame = pd.DataFrame(
            columns=['intent', 'expected', 'sentence', 'right', 'wrong', 'matched', 'complete'])

    def get_data_frame(self):
        return self._data_frame

    def user_update(self, sentence: str = None, right=None, wrong=None,
                    matched: bool = None, complete: float = None):
        if wrong is None:
            wrong = []
        if right is None:
            right = []
        self._data_frame.loc[self._data_frame.index[-1], ['sentence', 'right', 'wrong', 'matched', 'complete']] = [
            sentence, right, wrong,
            matched, complete]

    def system_update(self, intent: Intent, expected=None):
        self._data_frame.loc[self._data_frame.size, ['intent', 'expected']] = [intent, expected]


class DialogContextModel:
    memory = Memory()

    def __init__(self) -> None:
        super().__init__()
        self.context = None

    def __call__(self, *args, **kwargs):
        potion = random.choice(list(potions))
        if potion == 'polyjuice':
            self.context = frames.PolyjuiceFrame()
        elif potion == 'armadillo bile mixture':
            self.context = frames.ArmadilloBileMixtureFrame()
        elif potion == 'animagus':
            self.context = frames.AnimagusFrame()

    def process_input(self, sentence):
        intent = self.memory.get_data_frame()['intent'].values[-1]
        expected = self.memory.get_data_frame()['expected'].values[-1]
        subtrees = lu.parse_sentence(sentence)

        if lu.check_sentence(sentence):
            if intent == Intent.HANDSHAKE:
                self.memory.user_update(sentence=sentence)
                return
            elif intent == Intent.INGREDIENTS:
                right, wrong = [], []
                for tree in subtrees:
                    if tree in expected:
                        right.append(tree)
                        self.context.set_ingredient(frames.IngredientFrame(str(tree)))
                    elif tree in ingredients:
                        wrong.append(tree)
                self.memory.user_update(sentence=sentence, right=right, wrong=wrong, matched=len(right) > len(wrong),
                                        complete=self.context.is_complete())
                return
            elif intent == Intent.Y_N or intent == Intent.Y_N_INGREDIENT:
                positive_sentence = lu.is_positive(sentence)
                print(positive_sentence)
                if positive_sentence is not None:  # da rivedere
                    if intent == Intent.Y_N:
                        matched = (positive_sentence and expected == 'yes') or (
                                not positive_sentence and expected == 'no')
                        self.memory.user_update(sentence=sentence, matched=matched,
                                                complete=self.context.is_complete())
                    else:
                        matched = (positive_sentence == expected[0])
                        if positive_sentence and expected[0] is True:
                            self.context.set_ingredient(frames.IngredientFrame(expected[1]))
                        self.memory.user_update(sentence=sentence, matched=matched,
                                                complete=self.context.is_complete())
                else:
                    self.memory.user_update(sentence=sentence, matched=False,
                                            complete=self.context.is_complete())

