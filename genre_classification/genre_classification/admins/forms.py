from django import forms
from admins.models import SQLiteCollection


class CollectionForm(forms.ModelForm):
    class Meta:
        model = SQLiteCollection
        fields = ('document', )
