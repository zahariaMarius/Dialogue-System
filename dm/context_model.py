import random
from db.potion_dictionary import potions, ingredients, pos_words, neg_words
from dm import frames
from analysis import language_understanding as lu
import pandas as pd
import nltk
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

    def user_update(self, sentence: str = None, right: int = None, wrong: int = None,
                    matched: bool = None, complete: float = None):
        self._data_frame.loc[-1:, ['sentence', 'right', 'wrong', 'matched', 'complete']] = [sentence, right, wrong,
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

        match intent:
            case Intent.HANDSHAKE:
                self.memory.user_update(sentence=sentence)
                return
            case Intent.INGREDIENTS:
                subtrees = lu.parse_sentence(sentence)
                right = 0
                wrong = 0
                for tree in subtrees:
                    if tree in expected:
                        right += 1
                        self.context.set_ingredient(frames.IngredientFrame(str(tree)))
                    elif tree in ingredients:
                        wrong += 1
                self.memory.user_update(sentence=sentence, right=right, wrong=wrong, matched=right > wrong,
                                        complete=self.context.is_complete())
                return
            case 'yes_no':
                sentence = nltk.word_tokenize(sentence)
                pos, neg = 0, 0
                for word in sentence:
                    if word in neg_words:
                        neg += 1
                    elif word in pos_words:
                        pos += 1
                positive_sentence = pos > neg
                return
            case 'evaluation':
                return
