# Generated by Django 4.2.14 on 2024-08-17 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_subscriber_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='attachement',
            field=models.FileField(blank=True, upload_to='email_attachments/'),
        ),
    ]
