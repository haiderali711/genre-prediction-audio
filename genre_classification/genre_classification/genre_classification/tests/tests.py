from django.test import TestCase
from genre_classification.predict import predict

class PredictionTestCase(TestCase):
    def test_predict(self):
        prediction = predict("genre_classification/tests/test_song/blues_train.wav")
        self.assertEqual("blues", prediction)
    
    
    
    
    
