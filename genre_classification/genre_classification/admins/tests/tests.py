import shutil
from os import path

from admins.train_model import train, create_dirtree
from django.test import TestCase

model_name = "__test_model"
models_path = "admins/models/"


class PredictionTestCase(TestCase):
    def test_model_creation(self):
        self.clear_model()
        create_dirtree(model_name)
        train("admins/tests/test_db/genres.db", model_name)
        self.assertTrue(path.exists(models_path + model_name))

    def test_model_encoder(self):
        self.assertTrue(path.exists(models_path + model_name + "/label_encoder"))
        self.assertTrue(path.exists(models_path + model_name + "/label_encoder/classes.npy"))

    def test_model_scaler(self):
        self.assertTrue(path.exists(models_path + model_name + "/data_scaler"))
        self.assertTrue(path.exists(models_path + model_name + "/data_scaler/scaler.bin"))

    def test_model_prediction(self):
        self.assertTrue(path.exists(models_path + model_name + "/prediction_model"))
        self.assertTrue(path.exists(models_path + model_name + "/prediction_model/saved_model.pb"))

    def test_model_db(self):
        self.assertTrue(path.exists(models_path + model_name + "/database"))

    def clear_model(self):
        try:
            shutil.rmtree(models_path + model_name)
        except OSError as e:
            print("Error: %s : %s" % (models_path + model_name, e.strerror))
