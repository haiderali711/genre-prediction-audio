import joblib
import numpy as np
from django.shortcuts import render
from genre_classification.extract_features import extract
from genre_classification.forms import DocumentForm
from keras import models
from sklearn.preprocessing import LabelEncoder


def handle_file_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            filename = request.FILES['document']
            print("\n*************")
            print("Processing " + str(filename) + "...")
            print("*************\n")
            # Feature extraction
            tuple_data = extract(filename)

            # Load ML model from file
            try:
                model = models.load_model("genre_classification/models/model_1/prediction_model")

                # Convert tuple to numpy array
                track = np.asarray(tuple_data).astype(np.float)

                # Feature number of Columns
                n_features = track.shape[0]

                # Scale features before prediction by importing scaler
                scaler = joblib.load('genre_classification/models/model_1/data_scaler/scaler.bin')
                track_scaled = scaler.transform(track.reshape(1, -1))

                # Make prediction
                prediction = model.predict(track_scaled.reshape(-1, n_features))
                # Take the index of the prediction with highest certainty percentage
                prediction = np.argmax(prediction[0])

                # save np.load
                np_load_old = np.load

                # modify the default parameters of np.load
                np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)

                encoder = LabelEncoder()
                # Load encoder classes to retrieve the labels
                encoder.classes_ = np.load('genre_classification/models/model_1/label_encoder/classes.npy')

                # restore np.load for future normal usage
                np.load = np_load_old

                # Inverse transform to get the label
                # e = encoder
                prediction = encoder.inverse_transform([prediction])

                # p = e.inverse_transform([prediction])
                print(prediction)

                print("\n*************")
                print(filename, "is", prediction)
                print("*************\n")

                return render(request, 'genre_classification/predictions.html',
                              {'form': form, 'prediction': prediction[0]})

            except Exception as e:
                form = DocumentForm()
                return render(request, 'genre_classification/home.html',
                              {'form': form, 'error': e})
    else:
        form = DocumentForm()
    return render(request, 'genre_classification/home.html', {
        'form': form,
    })
