import os
import uuid

from django.db import models
from admins.data_validation import validate_db_extension

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(filename)

class MLModel(models.Model):
    model_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    accuracy = models.FloatField(null=True)
    no_of_tracks = models.IntegerField(null=True)
    # weights = models.
    active = models.BooleanField(null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.model_name

# Model for database file
# we actually do not .save() any of the database files to the django db
class MLModelFile(models.Model):
    db = models.FileField(upload_to=get_file_path, validators=[validate_db_extension], default=None)