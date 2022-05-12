import spacy
from spacy import displacy
from db.potion_dictionary import pos_words, neg_words, ingredients
from nltk.corpus import words, stopwords
from nltk import WordNetLemmatizer, word_tokenize
import string

stop = stopwords.words('english')
punct = string.punctuation + '’'
lemmatizer = WordNetLemmatizer()
nlp = spacy.load('en_core_web_trf')


def check_sentence(sentence):
    sentence = [lemmatizer.lemmatize(word) for word in word_tokenize(sentence.lower()) if word not in punct]
    bools = [word in words.words() or word in ingredients for word in sentence]
    return (sum(bools) / len(bools)) > 0.5


def parse_sentence(sentence):
    doc = nlp(sentence)
    ingredients = [np.text
                   for nc in doc.noun_chunks
                   for np in [nc, doc[nc.root.left_edge.i: nc.root.right_edge.i + 1]]]
    print(ingredients)
    return list(dict.fromkeys(ingredients))


def is_positive(sentence):
    pos, neg = 0, 0
    for word in word_tokenize(sentence):
        if word in neg_words:
            neg += 1
        elif word in pos_words:
            pos += 1
    if pos == neg:
        return None
    else:
        return pos > neg
