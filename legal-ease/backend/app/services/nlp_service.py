import spacy

nlp = spacy.load("en_core_web_sm")

def extract_sentences(text: str):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]