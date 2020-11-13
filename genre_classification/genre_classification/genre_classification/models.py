from django.db import models
from django.forms import ValidationError

class Document(models.Model):
    def validate_file_extension(value):
        if not value.name.endswith('.wav'):
            raise ValidationError(u'Only .wav files are allowed!')
    document = models.FileField(upload_to='', validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    
