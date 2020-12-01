from django import forms
from genre_classification.models import AudioFile


class DocumentForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ('document', )
