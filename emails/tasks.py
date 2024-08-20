# from the main project folder within CELERY.PY, we load the variable APP
from autocommontasks_main.celery import app
from dataentry.utils import send_email_notification


@app.task
def send_email_task(mail_subject, message_body, to_email_addresses, attachment):
    send_email_notification(mail_subject, message_body,
                            to_email_addresses, attachment)
    return 'Email sending task executed successfully.'
