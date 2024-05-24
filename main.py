# containing all funnction chatboot needed
import tensorflow as tf 
from tensorflow.keras.utils import pad_sequences
import pickle
import re
import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import json

def load_model_and_tokenizer(path: str): 
    # load tokenizer
    with open("./tokenizer.pickle", 'rb') as handle:
        tokenizer = pickle.load(handle)
    # load model
    model = tf.keras.models.load_model(path)
    # return model and tokenizer
    return model, tokenizer

def read_json(): 
    with open('./content.json', encoding='utf-8') as f:
        data = json.load(f)
    return data

# for prediction 
def predict_class(text: str, tokenizer, model): 
    factory = StemmerFactory()
    # stemmer 
    stemmer = factory.create_stemmer()
    text= text.lower()
    text= re.sub(r'\W', ' ', text)
    # delete number
    text= re.sub(r'\d+', '', text)
    # deleting punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # delete excessive whitespace
    text= re.sub(r'\s+', ' ', text)
    # stemming
    final_text= stemmer.stem(text)
    # text to sequences
    text_tokeneize = tokenizer.texts_to_sequences([final_text])
    # pad_sequnces
    text_tokeneize = pad_sequences(text_tokeneize)
    # predict
    pred = model.predict(text_tokeneize)
    return np.argmax(pred)

# nex to do : read dataset pegawai (connect to mysql)
