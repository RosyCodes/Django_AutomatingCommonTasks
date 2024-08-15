# from the project folder in CELERY.PY, we load the variable APP
from autocommontasks_main.celery import app
import time
from django.core.management import call_command
# from django.core.mail import EmailMessage
from django.conf import settings
from .utils import send_email_notification


@app.task  # uses a decorator as a celery task for testing
def celery_test_task():
    time.sleep(10)  # simulation of any task that's going to take 10 seconds
    # send an email
    mail_subject = 'Test subject'
    message_body = 'This is a test email.'
    # calls our default_to_email value from settings.py
    to_email_addresses = settings.DEFAULT_TO_EMAIL

    # we have a centralized EMAIL FUNCTION HELPER, so we dont need this block
    # ----
    # from_email = settings.DEFAULT_FROM_EMAIL # calls our default_from_email value from settings.py
    # mail = EmailMessage(mail_subject, message_body,
    #                     from_email, to=[to_email_addresses])
    # mail.send()  # sends our mail
    # ------

    # calls our EMAIL FUNCTION HELPER INSTEAD in UTILS.py
    send_email_notification(mail_subject, message_body, to_email_addresses)

    return ' Email Sent successfully.'


@app.task  # uses a decorator as a celery task for importing large data
def import_data_task(file_path, model_name):
    try:
        # trigger the custom-management import data command
        call_command('importdata', file_path, model_name)
        # passes this custom-made message to our web page
    except Exception as e:
        raise e
    # notify the user via email IF there is no error
    mail_subject = 'Import Data Completed'
    message_body = 'Your data import has been successfully completed.'
    # calls our default_to_email value from settings.py
    to_email_addresses = settings.DEFAULT_TO_EMAIL

    # calls our EMAIL FUNCTION HELPER INSTEAD in UTILS.py
    send_email_notification(mail_subject, message_body, to_email_addresses)
    # shows a message in the terminal
    return 'Data imported successfully.'
