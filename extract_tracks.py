import librosa
import numpy as np

# Extract features using librosa
def get_tracks(audio_file, path):
    # Import file mapping files to labels
    file1 = open(path + '/genres/input.mf', 'r')
    lines = file1.readlines()
    
    data = np.zeros((len(lines), 2))

    i = 0
    for line in lines:
        filename = line.strip().split("\t", 1)[0].split("/", 4)[4]
        genre = line.strip().split("\t", 1)[1]

        audio_file = path + "/" + filename
        y, sr = librosa.load(audio_file, mono=True, duration=30)
        data[i, 0] = y
        data[i, 1] = genre
        i++
        
