import os
import shutil
from pathlib import Path

from django.shortcuts import render, redirect

from .data_validation import validate_db
from .forms import RetrainForm, RetrainFormFile
from .models import MLModel
from .train_model import train, create_dirtree


def admin_view(request):
    # Retrieve list of models
    models = MLModel.objects.order_by('-created_on')
    errors = ''

    try:
        active_model = MLModel.objects.get(active=True)
    except Exception as e:
        active_model = None

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
            print('model', model.model_name)

            # Compile saved database path
            db_path = 'admins/models/' + str(model) + '/database/features.db'

            # Create the directory tree for the model
            try:
                create_dirtree(str(model))

                # Deactivate the previous model before setting the new one as active
                if active_model is not None:
                    deactivate_model(active_model.model_name)

                # File is not saved on disk so
                # -> Save uploaded db to file in the dedicated folder /models/{model}/database/features.db
                with open(db_path, 'wb+') as destination:
                    for chunk in db.chunks():
                        destination.write(chunk)  # Add exception try catch to delete created folders

                #######################
                ### Data Validation ###
                if validate_db(db_path):
                    print("Data validation has been passed")

                    # Train our model with the new data and retrieve accuracy and number of tracks
                    print("Starting retraining..")
                    accuracy, n_tracks = train(db_path, str(model))

                    print('Statistics for new model "' + str(model) + '":')
                    print("Accuracy:", accuracy)
                    print("Tracks:", n_tracks)

                    # Injecting model object with attributes that we now have
                    model.accuracy = accuracy * 100
                    model.no_of_tracks = n_tracks
                    model.active = True

                    active_model = model

                    # Committing model to django db
                    model.save()

                    # move the active model files to genre_classification/models/model_1
                    move_model_files(active_model.model_name)

                    print("New model saved!")

                else:
                    print("Data validation has not been passed")
                    raise Exception('The data is invalid (features are missing or malformed)')
            except Exception as e:
                errors = e

            return render(request, 'admins/admins.html',
                          {'models': models, 'errors': errors, 'active_model': active_model})

    return render(request, 'admins/admins.html',
                  {'models': models, 'errors': errors, 'active_model': active_model})


def activate_model(request):
    active_model_name = request.GET.get('active_model_name')
    model_name_to_activate = request.GET.get('model_name_to_activate')

    print(active_model_name, model_name_to_activate)

    deactivate_model(active_model_name)
    MLModel.objects.filter(model_name=model_name_to_activate).update(active=True)
    move_model_files(model_name_to_activate)

    return redirect('/admin')


def deactivate_model(model_name):
    MLModel.objects.filter(model_name=model_name).update(active=False)


# move the model folder to the applied model folder in genre classification folder
def move_model_files(model_name_to_activate):
    BASE_DIR = Path(__file__).resolve().parent.parent
    trained_path = os.path.join(BASE_DIR, ('admins/models/' + model_name_to_activate))
    destination_path = os.path.join(BASE_DIR, 'genre_classification/models/model_1')
    print('TRAINED : ', trained_path)
    print('DESTINATION : ', destination_path)

    # recursively remove contents of a dir
    try:
        shutil.rmtree(destination_path)
    except Exception as e:
        print('Delete Error', e)
    finally:
        # copy the new model in the folder
        shutil.copytree(trained_path, destination_path)
