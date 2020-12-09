from django.shortcuts import render
from django.utils import timezone

from .models import MLModel, MLModelFile
from .forms import RetrainForm, RetrainFormFile

from .train_model import train, create_dirtree

def admin_view(request):
    # Retrieve list of models
    models = MLModel.objects.order_by('-created_on')

    if request.method == 'POST':
        print("Retrain request received..")
        # 2 forms, one for the model_name and the other for the db file
        form = RetrainForm(request.POST, request.FILES)
        form_file = RetrainFormFile(request.POST, request.FILES)
        if form.is_valid() and form_file.is_valid():
            # Retrieve the db sitting in memory (not on disk)
            db = request.FILES['db']
            # Save the model without committing to db
            model = form.save(commit=False)

            # Compile saved database path
            db_path = 'admins/models/'+str(model)+'/database/features.db'

            # Create the directory tree for the model
            try:
                create_dirtree(str(model))
            except Exception as e:
                #TODO: manage exception, prompt user with error message instead of error page
                print("Aborting...")
                raise e


            # File is not saved on disk so
            # -> Save uploaded db to file in the dedicated folder /models/{model}/database/features.db
            with open(db_path, 'wb+') as destination:
                for chunk in db.chunks():
                    destination.write(chunk) #Add exception try catch to delete created folders

            # Train our model with the new data and retrieve accuracy and number of tracks
            print("Starting retraining..")
            accuracy, n_tracks = train(db_path, str(model))

            print('Statistics for new model "'+str(model)+'":')
            print("Accuracy:", accuracy)
            print("Tracks:", n_tracks)

            # Injecting model object with attributes that we now have  
            model.accuracy = accuracy
            model.no_of_tracks = n_tracks
            model.active = True
            # TODO: unactivate the previously active model 
            # Committing model to django db
            model.save()
            print("New model saved!")

            models = MLModel.objects.order_by('-created_on')
            return render(request, 'admins/admins.html', {'models': models})

    return render(request, 'admins/admins.html', {'models': models})

# def activate_model(request):
#     print("activate model called")
#     return render(request, 'admins/admins.html')
