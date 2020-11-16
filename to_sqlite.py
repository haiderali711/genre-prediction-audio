# SqLite dependencies
import sqlite3
import os

# Feature Extraction dependencies
import librosa
import numpy as np

# Remove db file on startup
try:
    os.remove("genres.db")
except:
    print("File does not exist")

# Connect / create database
con = sqlite3.connect('genres.db')

# Create table
cur = con.cursor()  # instantiate a cursor obj
create_table_sql = """
CREATE TABLE genrepath (
filename text PRIMARY KEY,
"""

# Build table
header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
for i in range(1, 21):
    header += f' mfcc{i}'
header += f' genre'
header = header.split()
for l in header[1:-1]:
    create_table_sql += l + " real, "
create_table_sql += "genre text)"

cur.execute(create_table_sql)

# Insert values
insert_sql = "INSERT INTO genrepath ("
insert_sql += str(header)[1:-1].replace("'", "")
insert_sql += ") VALUES ("
insert_sql += str(['?'] * len(header))[1:-1].replace("'", "")
insert_sql += ");"

# Import file mapping files to labels
file1 = open('genres/input.mf', 'r')
lines = file1.readlines()

for line in lines:
    filename = line.strip().split("\t", 1)[0].split("/", 4)[4]
    genre = line.strip().split("\t", 1)[1]
    print("Processing", filename, "...")

    # Extract features using librosa
    y, sr = librosa.load(filename, mono=True, duration=30)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)

    # Building tuple to insert
    tuple_data = f'{filename} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
    for e in mfcc:
        tuple_data += f' {np.mean(e)}'
    tuple_data += f' {genre}'
    tuple_data = tuple(tuple_data.split())

    # Inserting data
    cur.execute(insert_sql, tuple_data)

con.commit()
