from django import forms
from admins.models import MLModel, MLModelFile

class RetrainForm(forms.ModelForm):
    class Meta:
        model = MLModel
        fields = ('model_name', )

class RetrainFormFile(forms.ModelForm):
    class Meta:
        model = MLModelFile
        fields = ('db', )

