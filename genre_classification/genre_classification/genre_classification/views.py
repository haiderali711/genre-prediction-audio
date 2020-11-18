from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from genre_classification.forms import DocumentForm

import librosa
import numpy as np


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            filename = request.FILES['document']
            print(filename)

            #Feature extraction
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
            tuple_data = tuple(tuple_data.split())  
            print(tuple_data)
            
            #Prediction
            #prediction = predict(tuple_data)
            #return HttpResponse(prediction)
            prediction = "?"

            return render(request, 'genre_classification/predictions.html',{'form': form, 'prediction': prediction})
    else:
        form = DocumentForm()
    return render(request, 'genre_classification/home.html', {
        'form': form
    })
