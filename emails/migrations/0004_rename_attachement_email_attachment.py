# Generated by Django 4.2.14 on 2024-08-19 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_alter_email_attachement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='attachement',
            new_name='attachment',
        ),
    ]
