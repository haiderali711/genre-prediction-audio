from django.shortcuts import render
from .forms import DocumentForm
from .predict import predict

def handle_file_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            filename = request.FILES['document']
            print("\n*************")
            print("Processing " + str(filename) + "...")
            print("*************\n")
            
            prediction = predict(filename)

            print("\n*************")
            print(filename, "is", prediction)
            print("*************\n")

            return render(request, 'genre_classification/predictions.html', {'form': form, 'prediction': prediction})
    else:
        form = DocumentForm()
    return render(request, 'genre_classification/home.html', {
        'form': form
    })
