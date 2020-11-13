from django.shortcuts import render
from django.http import HttpResponse

from genre_classification.models import Document
from genre_classification.forms import DocumentForm

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('The file is saved')
    else:
        form = DocumentForm()
    return render(request, '../templates/home.html', {
        'form': form
    })
