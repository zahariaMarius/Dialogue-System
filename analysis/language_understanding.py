import spacy


def parse_sentence(sentence):
    nlp = spacy.load('en_core_web_trf')
    doc = nlp(sentence)
    print()
    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_,
              chunk.root.head.text)

    displacy.serve(doc, host='127.0.0.1', style='dep')
