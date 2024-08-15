from django.shortcuts import render, redirect
from .utils import get_all_custom_models, check_csv_error
from uploads.models import Upload
from django.conf import settings
from django.contrib import messages
# imports our celery function
from .tasks import import_data_task


def import_data(request):
    if request.method == 'POST':
        # gets the user-submitted file using its path
        file_path = request.FILES.get('file_path')
        # gets the user-submitted MODEL name
        model_name = request.POST.get('model_name')

        # store this file inside the Upload model
        upload = Upload.objects.create(file=file_path, model_name=model_name)

        # construct the full path of the file with the file_path for import
        relative_path = str(upload.file.url)
        # gets the directory of our root directory
        base_url = str(settings.BASE_DIR)

        file_path = base_url + relative_path  # absolute path of the file

        # check for the CSV errors, if there is an error, we wont call our celery function for import
        try:
            # calls the check_csv_error function in dataentry\utils.property
            check_csv_error(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')

        # if no error, call the Celery function for data import from dataentry\tasks.py
        import_data_task.delay(file_path, model_name)

        # show the message the user
        messages.success(
            request, 'Your data is being imported, you will be notified once this ia done.')
        return redirect('import_data')
    else:
        # calls our dataentry\utils.py to extract only user-created models
        custom_models = get_all_custom_models()
        # print(custom_models)
        context = {
            'custom_models': custom_models,
        }
    return render(request, 'dataentry/importdata.html', context)
