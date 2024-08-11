from django.shortcuts import render, redirect
from .utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages


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

        # trigger the custom-management import data command
        try:
            call_command('importdata', file_path, model_name)
            # passes this custom-made message to our web page
            messages.success(
                request, 'You have successfully imported the file.')
        except Exception as e:
            # raise e
            # passes this error type  to our web page
            messages.error(request, str(e))

        return redirect('import_data')
    else:
        # calls our dataentry\utils.py to extract only user-created models
        custom_models = get_all_custom_models()
        # print(custom_models)
        context = {
            'custom_models': custom_models,
        }
    return render(request, 'dataentry/importdata.html', context)
