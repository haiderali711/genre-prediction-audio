import os
import sys
import sqlite3
from extract_features import extract

if len(sys.argv) == 1:
    path = ""
else:
    path = sys.argv[1]

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

# Insert values
insert_sql = "INSERT INTO genrepath ("
insert_sql += str(header)[1:-1].replace("'", "")
insert_sql += ") VALUES ("
insert_sql += str(['?'] * len(header))[1:-1].replace("'", "")
insert_sql += ");"

# Import file mapping files to labels
file1 = open(path + '/genres/input.mf', 'r')
lines = file1.readlines()

for line in lines:
    filename = line.strip().split("\t", 1)[0].split("/", 4)[4]
    genre = line.strip().split("\t", 1)[1]
    print("Processing" + path + "/" + filename, "...")

    # Extract features using librosa
    tuple_data = extract(path + "/" + filename)
    to_db = tuple({filename}) + tuple_data + tuple({genre})

    # Inserting data
    cur.execute(insert_sql, to_db)

con.commit()
