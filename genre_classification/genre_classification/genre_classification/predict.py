import joblib
import numpy as np
from keras import models
from sklearn.preprocessing import LabelEncoder


def predict(tuple_data, type_user):
    # Load ML model from file
    if type_user == 'user':
        model = models.load_model(
            "genre_classification/user_data/retrained/prediction_model")
    else:
        model = models.load_model(
            "genre_classification/models/model_1/prediction_model")

    # Convert tuple to numpy array
    track = np.asarray(tuple_data).astype(np.float)

    # Feature number of Columns
    n_features = track.shape[0]

    # Scale features before prediction by importing scaler
    if type_user == 'user':
        scaler = joblib.load(
            'genre_classification/user_data/retrained/data_scaler/scaler.bin')
    else:
        scaler = joblib.load(
            'genre_classification/models/model_1/data_scaler/scaler.bin')
    track_scaled = scaler.transform(track.reshape(1, -1))

    # Make prediction
    prediction = model.predict(track_scaled.reshape(-1, n_features))
    # Normalization of the prediction values from 1-100
    norm_pred = prediction_values_normalized(10000, prediction[0])
    norm_pred = np.array(norm_pred).astype(int)
    norm_pred = norm_pred / 100

    # Take the index of the prediction with highest certainty percentage
    prediction = np.argmax(prediction[0])

    # save np.load
    np_load_old = np.load

    # modify the default parameters of np.load
    np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)

    encoder = LabelEncoder()
    # Load encoder classes to retrieve the labels
    if type_user == 'user':
        encoder.classes_ = np.load(
            'genre_classification/user_data/retrained/label_encoder/classes.npy')
    else:
        encoder.classes_ = np.load(
            'genre_classification/models/model_1/label_encoder/classes.npy')

    # restore np.load for future normal usage
    np.load = np_load_old

    # Inverse transform to get the label
    prediction = encoder.inverse_transform([prediction])[0]

    # Labeling the percentage of each prediction
    label_percentages = np.array([[]])
    index = 0
    for norm in norm_pred:
        label_percentages = np.append(label_percentages, np.array([encoder.inverse_transform([index])[0], norm]))
        index += 1
    label_percentages = np.reshape(label_percentages, (10, 2))
    # we are sending both predicted label and it's percentage
    max_perc = 0
    for label in label_percentages:
        if label[0] == prediction:
            max_perc = label[1]

    predicted_label = {'label': prediction, 'percentage': max_perc}

    # Sort the numpy array in descending order according to the second column
    label_percentages = label_percentages[label_percentages[:, 1].argsort()[::-1]]
    print("label_ percentages", label_percentages)

    return predicted_label, label_percentages


def prediction_values_normalized(range, prediction):
    max_pred = max(prediction)
    min_pred = min(prediction)
    print(max_pred, min_pred, "newprint")
    norm_pred = []
    for item in prediction:
        norm_pred.append(range * ((item - min_pred) / (max_pred - min_pred)))

    return norm_pred
