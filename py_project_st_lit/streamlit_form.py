import streamlit as st
import spacy 

nlp = spacy.load('en_core_web_lg')

def extract_entities(ent_types, text):

    results = []

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ent_types:
            results.append((ent.text, ent.label_))
    return()