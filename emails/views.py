from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber, Email, Sent, EmailTracking
from .tasks import send_email_task
from django.db.models import Sum
from django.utils import timezone

from django.http import HttpResponse, HttpResponseRedirect


def send_email(request):
    if request.method == 'POST':
        # gets the user - provided values from the Email form
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email = email_form.save()
            # Send an email using the email helper from DATAENTRY\UTILS.PY
            mail_subject = request.POST.get('subject')
            message_body = request.POST.get('body')

            # Send to our default recipient
            # to_email_addresses = settings.DEFAULT_TO_EMAIL
            # Get the FK ID of the email group of subscribers
            email_list = request.POST.get('email_list')

            # Get the selected email list or group name
            email_list = email.email_list

            # Extract email addresses from the Subscriber model
            subscribers = Subscriber.objects.filter(email_list=email_list)
            # GOOD OPTION: adds each email
            # to_email_addresses = []
            # for email in subscribers:
            #     to_email_addresses.append(email.email_address)
            # OPTIMIZED OPTION: adds each email
            to_email_addresses = [email.email_address for email in subscribers]

            # check for email attachment
            if email.attachment:
                attachment = email.attachment.path
            else:
                attachment = None

            email_id = email.id
            # Handover instead the email-sending task to celery in tasks.py
            send_email_task.delay(mail_subject, message_body,
                                  to_email_addresses, attachment, email_id)
            # Without celery email function, call directly this function
            # send_email_notification(
            #     mail_subject, message_body, to_email_addresses, attachment)
            messages.success(request, 'Email sent successfully.')
            return redirect('send_email')
        return
    else:
        email = EmailForm()
        context = {
            'email_form': email,
        }
        return render(request, 'emails/send-email.html', context)


def track_click(request, unique_id):
    # logic to store the tracking
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        # the original link the user has provided in the email
        url = request.GET.get('url')
        # check if the clicked_at field is already set or not
        if not email_tracking.clicked_at:
            email_tracking.clicked_at = timezone.now()
            email_tracking.save()
            return HttpResponseRedirect(url)
        else:
            return HttpResponse(url)
    except:
        return HttpResponse('Email tracking record not found.')


def track_open(request, unique_id):
    # logic to store the tracking
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        # check if the opened_at field is already set or not not
        if not email_tracking.opened_at:
            email_tracking.opened_at = timezone.now()
            email_tracking.save()
            return HttpResponse('Email opened successfully.')
        else:
            print("Email already opened.")
            return HttpResponse('Email already opened.')
    except:
        return HttpResponse('Email tracking record not found.')


def track_dashboard(request):
    # add the total_sent field of SENT model as  annotations or addition to each record in our query set
    emails = Email.objects.all().annotate(
        total_sent=Sum('sent__total_sent')).order_by('-sent_at')

    context = {
        'emails': emails,
    }
    # logic to store the tracking
    return render(request, 'emails/track_dashboard.html', context)


def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    sent = Sent.objects.get(email=email)
    context = {
        'email': email,
        'total_sent': sent.total_sent,
    }
    return render(request, 'emails/track_stats.html', context)
