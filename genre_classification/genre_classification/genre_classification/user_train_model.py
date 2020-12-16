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





def create_db_connection(db_file):
    """
    Create a database connection to the SQLite database
    specified by the db_file
    
    :param db_file: database file
    :return: Connection object or None
    """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return connection


def create_folder(folder):
    try:
        os.mkdir(folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise





def create_dirtree(model_name):
    ###########################
    ### Step 1: Create dirs ###
    ###########################
    root_path = 'admins/models'
    model_path = os.path.join(root_path, model_name)
    
    create_folder(root_path)    
    try:
        os.mkdir(model_path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            raise Exception("Model already exists!")

    folders = ['data_scaler','database','label_encoder','prediction_model']
    for folder in folders:
        create_folder(os.path.join(model_path,folder))


def train(db, model_name):    
    ############################################
    ### Step 2: Retrieve data from SQLite db ###
    ############################################

    ## Get data from Database
    db_connection = create_db_connection(db) # can be None!

    # Read data as Pandas DataFrame
    genres_data = pd.read_sql_query("SELECT * from genrepath", db_connection)
    # Remove unnecessary data like 'filename'
    genres_data = genres_data.drop('filename', axis=1)

    # Encode Labels
    genres_list = genres_data.iloc[:,-1]
    encoder = LabelEncoder()
    y = encoder.fit_transform(genres_list)

    # Replace genres from 'genres_data' with encoded labels
    genres_data['genre'] = y

    ############################
    ### Step 3: Save encoder ###
    ############################

    np.save(f'admins/models/{model_name}/label_encoder/classes.npy', encoder.classes_)

    #############################################
    ### Step 4: Transform and select features ###
    #############################################

    # Separating features and target variable
    train_data_features = genres_data.drop('genre', axis =1)

    train_data_target = genres_data["genre"].copy()
    train_data_target.columns = ['genre']

    # Convert this to a Pandas DataFrame
    train_data_target = pd.DataFrame(train_data_target)

    ##############################
    ### Step 5: Scale features ###
    ##############################
    cols = train_data_features.columns

    #scaler = preprocessing.MinMaxScaler()  # alternative scaler
    scaler = StandardScaler()
    np_scaled = scaler.fit_transform(train_data_features)

    # new data frame with the new scaled data. 
    X = pd.DataFrame(np_scaled, columns = cols)

    ###########################
    ### Step 6: Save scaler ###
    ###########################

    joblib.dump(scaler, f'admins/models/{model_name}/data_scaler/scaler.bin', compress=True)

    ###########################
    ### Step 7: Train model ###
    ###########################

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=1) #Set random_state to None for randomized

    #Further split the training data into training and cross-validation datasets
    partial_X_train, X_val, partial_y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=0)


    model = models.Sequential()
    model.add(layers.Dense(512, activation='relu', input_shape=(X_train.shape[1],)))

    model.add(layers.Dense(256, activation='relu'))

    model.add(layers.Dense(128, activation='relu'))

    model.add(layers.Dense(64, activation='relu'))

    model.add(layers.Dense(10, activation='softmax'))

    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    print("Training prediction model...")
    history = model.fit(partial_X_train,
                        partial_y_train,
                        epochs=30,
                        batch_size=128,
                        validation_data=(X_val, y_val),
                        verbose=0)
    print("Done")

    ###########################
    ### Step 7: Save model ###
    ###########################

    print("Saving prediction model...")
    model.save(f'admins/models/{model_name}/prediction_model')
    print("Done")

    test_loss, test_acc = model.evaluate(X_test,y_test)

    return test_acc, y.shape[0]