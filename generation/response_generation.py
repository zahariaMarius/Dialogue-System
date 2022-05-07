import simplenlg
from simplenlg.framework import *
from simplenlg.lexicon import *
from simplenlg.realiser.english import *
from simplenlg.phrasespec import *
from simplenlg.features import *
import random


class ResponseGenerator:
    lexicon = Lexicon.getDefaultLexicon()
    nlgFactory = NLGFactory(lexicon)
    realiser = Realiser(lexicon)

    def __init__(self) -> None:
        super().__init__()

    def evaluate(self):
        return 10

    def initiate_exam(self, potion):
        return "Mr Potter, tell me the ingredients for " + potion + " potion"

    # per risposte parzialmente giuste (o mancano ingredienti o alcuni sono giusti e altri no)
    def clarify(self, data_frame, expected):
        # if intent == 'ingredient':
            ing = self.nlgFactory.createNounPhrase('amorentia')
            ing.addPreModifier('sure about')
            clause = self.nlgFactory.createClause('you', 'be', ing)
            clause.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
            return str(self.realiser.realise(clause))

    # per risposte giuste
    def approval(self):
        answer = ['Good job Potter, I definitely was not expecting this result from you',
                  'Well, well Potter, I must congratulate you. It seems like your friendship with miss Granger is paying off after all',
                  'It seems like you have gotten all the ingredients right Potter',
                  'It is easy to see that nearly six years of magical education have not been wasted on you, Potter',
                  'You guessed all the ingredients Potter, after all I would expect nothing less from a celebrity like you'][
            random.randrange(5)]

        evaluation = self.evaluate()
        answer += 'Your final evaluation for the class of Potions is' + str(evaluation)
        return answer

    # per risposte sbagliate
    def refusal(self):
        answer = ['Mr Potter I remind you this is not Defence against the Dark Arts',
                  'Answers like this will cost some points to your House',
                  'Mr Potter you better concentrate if you don\'t want me to take away points from Gryffindor',
                  'How extraordinarily like your father you are, Potter. He too was exceedingly bad at potions'][
            random.randrange(4)]
        answer += ', I suggest you tell me some ingredients'
        return answer

    def greeting(self, potion):
        return "Welcome Mr. Potter"
