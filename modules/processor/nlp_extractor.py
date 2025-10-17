import spacy
import json

nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str) -> str:
    doc = nlp(text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    return json.dumps(entities, indent=2)
