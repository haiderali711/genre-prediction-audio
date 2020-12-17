import os
import errno
import shutil
import sqlite3
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from keras import models
from keras import layers
from keras import callbacks
from django.shortcuts import render
from .forms import DocumentForm
from .predict import predict

def handle_file_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            filename = request.FILES['document']
            print("\n*************")
            print("Processing " + str(filename) + "...")
            print("*************\n")
           
            try:
                 # Feature extraction
                prediction,label_percentages,tuple_data = predict(filename)

                print("\n*************")
                print(filename, "is", prediction)
                print("*************\n")

                check_user_data_db()


                return render(request, 'genre_classification/predictions.html',
                              {'form': form, 'prediction': prediction , 'label_percentages': label_percentages, 'tuple_data': tuple_data})

            except Exception as e:
                form = DocumentForm()
                print(e)
                return render(request, 'genre_classification/home.html',
                              {'form': form, 'error': e})
    else:
        form = DocumentForm()
    return render(request, 'genre_classification/home.html', {
        'form': form,
    })




def check_user_data_db():
    BASE_DIR = Path(__file__).resolve().parent.parent
    db_destination = os.path.join(BASE_DIR, 'admins/user_data/user_data.db')
    print('Thjis is the directory : ',db_destination)

    try:
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
    except Exception as e:
        print(e)
