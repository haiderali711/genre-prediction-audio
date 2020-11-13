from django import forms
from genre_classification.models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document', )
