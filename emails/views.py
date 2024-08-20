from django.shortcuts import render, redirect
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber
from .tasks import send_email_task

# Create your views here.


def send_email(request):
    if request.method == 'POST':
        # gets the user - provided values from the Email form
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()
            # Send an email using the email helper from DATAENTRY\UTILS.PY
            mail_subject = request.POST.get('subject')
            message_body = request.POST.get('body')

            # Send to our default recipient
            # to_email_addresses = settings.DEFAULT_TO_EMAIL

            # Get the FK ID of the email group of subscribers
            email_list = request.POST.get('email_list')

            # Get the selected email list or group name
            email_list = email_form.email_list

            # Extract email addresses from the Subscriber model
            subscribers = Subscriber.objects.filter(email_list=email_list)
            # GOOD OPTION: adds each email
            # to_email_addresses = []
            # for email in subscribers:
            #     to_email_addresses.append(email.email_address)

            # OPTIMIZED OPTION: adds each email
            to_email_addresses = [email.email_address for email in subscribers]

            # check for email attachment
            if email_form.attachment:
                attachment = email_form.attachment.path
            else:
                attachment = None

            # Handover instead the email-sending task to celery in tasks.py
            send_email_task.delay(mail_subject, message_body,
                                  to_email_addresses, attachment)

            # Without celery email function, call directly this function
            # send_email_notification(
            #     mail_subject, message_body, to_email_addresses, attachment)

            messages.success(request, 'Email sent successfully.')
            return redirect('send_email')
        return
    else:
        email_form = EmailForm()
        context = {
            'email_form': email_form,
        }
        return render(request, 'emails/send-email.html', context)
