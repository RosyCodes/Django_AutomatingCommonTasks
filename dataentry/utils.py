from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os

# extracts only the user-created models
# excludes default models like Users, etc


def get_all_custom_models():
    # lists the default models that we dont want to display in our Upload Form
    default_models = ['ContentType', 'Session',
                      'LogEntry', 'Group', 'Permission', 'User', 'Upload']

    custom_models = []
    for model in apps.get_models():
        # print(model.__name__)
        # checks if the model name is in the list of  default model or not
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
        # print(model)
    return custom_models


# celery custom function to check for errors before Celery does its task
def check_csv_error(file_path, model_name):
    # search for the model across all intalled apps
    target_model = None
    for my_app_config in apps.get_app_configs():
        # Try to search for the target model where we will save our imported data
        try:
            # returns the model name  of the app
            target_model = apps.get_model(my_app_config.label, model_name)
            break  # stops search once the model is found
        except LookupError:
            continue  # model is not found, then keep searching in the next app
    # if model is empty/not found
    if not target_model:
        raise CommandError(f'Model "{model_name}" not found in any app.')

    # get all the field names of the model that we found EXCEPT THE PK or ID
    model_fields = [field.name for field in target_model._meta.fields if field.name !=
                    'id']
    # print(model_fields)
    try:
        # opens the file for reading and closes it automatically
        with open(file_path, 'r') as file:
            # reads the csv file including the header
            reader = csv.DictReader(file)
            # gets the header names of the csv file
            csv_header = reader.fieldnames
            # compare CSV header with the model's field names and throw appropriate message
            if csv_header != model_fields:
                raise DataError(
                    f'CSV file does not match with the {model_name} table fields')
    except Exception as e:
        raise e
    # if there is no error, we return the model name
    return target_model

# sends an email with dynamic subject, message and recipient's address
# Attachment as an optional value


def send_email_notification(mail_subject, message_body, to_email_addresses, attachment=None):
    try:
        # calls our environment varialbe. DEFAULT_FROM_EMAIL from settings.py
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message_body,
                            from_email, to=to_email_addresses)
        # if file is present as part of our parameters.
        if attachment is not None:
            mail.attach_file(attachment)

        # send the mail as HTML content without the HTML tags
        mail.content_subtype = "html"
        
        mail.send()  # sends our mail
    except Exception as e:
        raise e

# create a csv file name for data export


def generate_csv_file(model_name):
    # generate the timestamp of current data and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # create a destination directory variable for our exported files
    export_dir = 'exported_data'  # name of our folder

    # export from any given table as a dynamic name.
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    # combines our MEDIA_ROOT directory with the export_dir and the filename
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    # print('File path - > ', file_path)
    return file_path
