import spacy
from spacy import displacy
from db.potion_dictionary import pos_words, neg_words
from nltk.corpus import words, stopwords
from nltk import WordNetLemmatizer, word_tokenize
import string

stop = stopwords.words('english')
punct = string.punctuation + '’'
lemmatizer = WordNetLemmatizer()


def check_sentence(sentence):
    sentence = [lemmatizer.lemmatize(word) for word in word_tokenize(sentence.lower()) if word not in punct]
    bools = [word in words.words() for word in sentence]
    score = (sum(bools) / len(bools)) > 0.5
    print(sentence)
    print()
    print(sum(bools) / len(bools))
    print()
    print(bools)
    return score

def parse_sentence(sentence):
    nlp = spacy.load('en_core_web_trf')
    doc = nlp(sentence, disable=['ner', 'lemmatizer', 'textcat'])

    ingredients = [np.text
                   for nc in doc.noun_chunks
                   for np in [nc, doc[nc.root.left_edge.i: nc.root.right_edge.i + 1]]]
    return list(dict.fromkeys(ingredients))
