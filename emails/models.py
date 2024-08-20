from django.db import models
from ckeditor.fields import RichTextField


class List(models.Model):
    # this is the email list
    email_list = models.CharField(max_length=25)

    def __str__(self):
        return self.email_list


class Subscriber(models.Model):
    # this email address can be part of any List
    email_list = models.ForeignKey(List, on_delete=models.CASCADE)
    email_address = models.EmailField(max_length=50)

    def __str__(self):
        return self.email_address


class Email(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE)
    # this is for the actual email message sent to the suscribers
    subject = models.CharField(max_length=100)
    body = RichTextField()
    # directs all email attached files to this folder
    attachment = models.FileField(upload_to='email_attachments/', blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
