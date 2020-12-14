import sqlite3
from django.forms import ValidationError

def get_labels(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.execute('select * from genrepath')
    features = [description[0] for description in cursor.description]
    features.remove('filename')
    features.remove('genre')
    return features

# Validate the newly uploaded model (extension)
def validate_db_extension(value):
        if not value.name.endswith('.db'):
            raise ValidationError(u'Only .db files are allowed!')

# Validate the newly uploaded model
def validate_db(db_path):
    try:
        current_features = get_labels('genre_classification/models/model_1/database/genres.db')
    except Exception as e:
        print(e)
        # Return true as there is no current trained model and the new DB passes directly the data validation
        return True
    try:
        new_features = get_labels(db_path)
        return set(current_features) == set(new_features)
    except Exception as e:
        print(e)
        # Return false as there is some problem, the db of the new trained model should exist
        return False
        
# Validate the uploaded song 
def validate_song(value):
    if not value.name.endswith('.wav'):
        raise ValidationError(u'Only .wav files are allowed!')