import os
import errno
import shutil
from pathlib import Path

import sqlite3
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler 
from sklearn.linear_model import LinearRegression
from sklearn import metrics

from keras import models
from keras import layers
from keras import callbacks

import joblib



def check_user_data_db():
    BASE_DIR = Path(__file__).resolve().parent.parent
    db_destination = os.path.join(BASE_DIR, 'genre_classification/models/user_model/user_data.db')

    # Connect / create database
    con = sqlite3.connect(db_destination)

    # Create table
    cur = con.cursor()  # instantiate a cursor obj
    create_table_sql = """
    CREATE TABLE genrepath (
    filename text PRIMARY KEY,
    """

    # Build table
    header = 'filename '
    header += 'chroma_stft_mean chroma_stft_var '
    header += 'rmse_mean rmse_var '
    header += 'spectral_centroid_mean spectral_centroid_var '
    header += 'spectral_bandwidth_mean spectral_bandwidth_var '
    header += 'rolloff_mean rolloff_var '
    header += 'zero_crossing_rate_mean zero_crossing_rate_var '
    header += 'harmonics_mean harmonics_var '
    header += 'perceptual_mean perceptual_var '
    header += 'tempo '
    for i in range(1, 21):
        header += f' mfcc{i}_mean mfcc{i}_var'
    header += f' genre'
    header = header.split()
    for l in header[1:-1]:
        create_table_sql += l + " real, "
    create_table_sql += "genre text)"

    cur.execute(create_table_sql)

def add_tuple_user_db (filename, tuple_data , genre): 
    BASE_DIR = Path(__file__).resolve().parent.parent
    db_destination = os.path.join(BASE_DIR, 'genre_classification/models/user_model/user_data.db')

    # Connect / create database
    con = sqlite3.connect(db_destination)
    cur = con.cursor() 

    # to_db = tuple({filename}) + tuple_data + tuple({genre})

    # Inserting data
    # cur.execute(insert_sql, to_db)


