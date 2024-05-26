# containing all funnction chatboot needed
import tensorflow as tf 
from tensorflow.keras.utils import pad_sequences
import pickle
import re
import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import json
import mysql.connector
import pandas as pd


def load_model_and_tokenizer(path: str): 
    # load tokenizer
    with open("./tokenizer.pickle", 'rb') as handle:
        tokenizer = pickle.load(handle)
    # load model
    model = tf.keras.models.load_model(path)
    # return model and tokenizer
    return model, tokenizer


def connect_database(): 
    try: 
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "")
        if mydb: 
            print("sucessfully conect to database")
            return mydb
        else: 
            raise ValueError("cant connect to database")
    except mysql.connector.Error as err: 
        print(f'errror : {err}')
        return None


def get_data_pegawai(): 
    mydb = connect_database()
    cursor = mydb.cursor()
    cursor.execute("use pkl;")
    cursor.execute("select * from pegawai;")
    data_pegawai = cursor.fetchall()
    return pd.DataFrame(data_pegawai, columns=['id', "name", "email"])

def insert_absensi(id_pegawai : int, date, name, message, attendance_type):
    mydb = connect_database()
    cursor = mydb.cursor()
    cursor.execute("use pkl;")
    sql = "INSERT INTO absensi (id_pegawai, date, name, message, attendance_type) VALUES (%s, %s, %s, %s, %s)"
    val = (id_pegawai, date, name, message, attendance_type)
    cursor.execute(sql, val)
    mydb.commit() 
    print("sucesfully insert to database!")



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
