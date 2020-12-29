from django.db import models
from admins.data_validation import validate_song


class AudioFile(models.Model):
    document = models.FileField(upload_to='', validators=[validate_song])
    uploaded_at = models.DateTimeField(auto_now_add=True)