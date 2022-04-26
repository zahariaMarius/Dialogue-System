from analysis import speech_recognizer as sr
from analysis import language_understanding as lu
from db import potion_dictionary as pd
from dm import frames

if __name__ == '__main__':
    sentence = 'the main ingredients are fluxweed, knotgrass and lacewing flies'
    #lu.parse_sentence(sentence)

    print(pd.potions['polyjuice'])

    juice = frames.PotionFrame('polyjuice', len(pd.potions['polyjuice']))

    print(type(juice.name))
    print(juice.ingredients)
    print(type(juice.ingredients[0]))
    juice.ingredients[0] = frames.IngredientFrame('weed')
    print(type(juice.ingredients[0]))
    print(isinstance(juice.ingredients[0], frames.IngredientFrame))

