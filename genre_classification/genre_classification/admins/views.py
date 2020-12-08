from django.shortcuts import render
from django.utils import timezone

from admins.models import MLModel
from admins.forms import CollectionForm

def admin_view(request):
    models = MLModel.objects.order_by('-created_on')
    return render(request, 'admins/admins.html', {'models': models})

def handle_file_upload(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST, request.FILES)
        if form.is_valid():
            
            return render(request, 'genre_classification/predictions.html', {'form': form, 'prediction': prediction})
    else:
        form = DocumentForm()
    return render(request, 'genre_classification/home.html', {
        'form': form
    })


# def activate_model(request):
#     print("activate model called")
#     return render(request, 'admins/admins.html')
