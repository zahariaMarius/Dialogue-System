import random
from db.potion_dictionary import potions, ingredients
from dm import frames
from analysis import language_understanding as lu
import pandas as pd

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
        self._data_frame = pd.DataFrame(columns=['sentence', 'right', 'wrong', 'complete'])

    def get_data_frame(self):
        return self._data_frame

    def update(self, sentence: str, right: int, wrong: int, complete: float):
        self._data_frame.loc[self._data_frame.size] = [sentence, right, wrong, complete]


class DialogContextModel:
    memory = Memory()

    def __init__(self) -> None:
        super().__init__()
        self.context = None

    def __call__(self, *args, **kwargs):
        potion = random.choice(list(potions))
        ingredients = potions[potion]

        if potion == 'polyjuice':
            self.context = frames.PolyjuiceFrame()
        elif potion == 'armadillo bile mixture':
            self.context = frames.ArmadilloBileMixtureFrame()
        elif potion == 'animagus':
            self.context = frames.AnimagusFrame()

    def process_input(self, sentence):
        subtrees = lu.parse_sentence(sentence)
        right = 0
        wrong = 0
        for tree in subtrees:
            if tree in potions[self.context.name]:
                right += 1
                self.context.set_ingredient(frames.IngredientFrame(str(tree)))
            elif tree in ingredients:
                wrong += 1
        print(self.context.show_attributes())
        self.memory.update(sentence, right, wrong, self.context.is_complete())
