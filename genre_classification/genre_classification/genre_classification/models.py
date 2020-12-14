from django.db import models
from admins.data_validation import validate_song

class AudioFile(models.Model):
    document = models.FileField(upload_to='', validators=[validate_song])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
class Predictions(models.Model):
    chroma_stft = models.FloatField()
    rmse = models.FloatField()
    spectral_centroid = models.FloatField()
    spectral_bandwidth = models.FloatField()
    rolloff = models.FloatField()
    zero_crossing_rate = models.FloatField()
    mfcc1 = models.FloatField()
    mfcc2 = models.FloatField()
    mfcc3 = models.FloatField()
    mfcc4 = models.FloatField()
    mfcc5 = models.FloatField()
    mfcc6 = models.FloatField()
    mfcc7 = models.FloatField()
    mfcc8 = models.FloatField()
    mfcc9 = models.FloatField()
    mfcc10 = models.FloatField()
    mfcc11 = models.FloatField()
    mfcc12 = models.FloatField()
    mfcc13 = models.FloatField()
    mfcc14 = models.FloatField()
    mfcc15 = models.FloatField()
    mfcc16 = models.FloatField()
    mfcc17 = models.FloatField()
    mfcc18 = models.FloatField()
    mfcc19 = models.FloatField()
    mfcc20 = models.FloatField()
    predicted_genre = models.IntegerField() 

    #Create a method to retun a string with actual sale price when querying the objects
    def __str__(self):
        return self.predicted_price