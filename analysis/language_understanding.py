import spacy
from spacy import displacy


def parse_sentence(sentence):
    nlp = spacy.load('en_core_web_trf')
    doc = nlp(sentence, disable=['ner', 'lemmatizer', 'textcat'])

    ingredients = [np.text
                   for nc in doc.noun_chunks
                   for np in [nc, doc[nc.root.left_edge.i: nc.root.right_edge.i + 1]]]
    return list(dict.fromkeys(ingredients))
