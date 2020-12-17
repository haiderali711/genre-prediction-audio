from django.test import TestCase
from .test_predict import predict

class PredictionTestCase(TestCase):
    def test_predict(self):
        prediction, label_percentages, tuple_data = predict("genre_classification/tests/test_song/blues_train.wav")
        self.assertEqual("blues", prediction['label'])