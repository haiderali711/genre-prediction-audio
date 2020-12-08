import os

from django.db import models
from django.forms import ValidationError 

class MLModel(models.Model):
    def validate_file_extension(value):
        if not value.name.endswith('.db'):
            raise ValidationError(u'Only .db files are allowed!')
    
    file_name = models.FilePathField()
    db = models.FileField(upload_to='', validators=[validate_file_extension])
    created_on = models.DateTimeField(auto_now_add=True)
    accuracy = models.FloatField()
    no_of_tracks = 888
    # weights = models.
    active = models.BooleanField()

    def __init__(self, file_name, db_file_name, created_on, accuracy, no_of_tracks, active, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_name = file_name
        self.db_file_name = db_file_name
        self.created_on = created_on
        self.accuracy = accuracy
        self.no_of_tracks = no_of_tracks
        self.active = active

    def activate(self):
        model_file = os.open(self.file_name.__str__(), os.O_RDONLY)
        self.active = True
        print(model_file)

    def deactivate(self):
        self.active = False

    def get_accuracy(self):
        return self.accuracy

    def get_no_of_tracks(self):
        return self.no_of_tracks

    def __str__(self):
        return self.file_name
