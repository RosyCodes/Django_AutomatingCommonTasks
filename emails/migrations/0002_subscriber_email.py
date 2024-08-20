# Generated by Django 4.2.14 on 2024-08-17 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.EmailField(max_length=50)),
                ('email_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emails.list')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('body', models.TextField(max_length=500)),
                ('attachement', models.FileField(upload_to='email_attachments/')),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('email_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emails.list')),
            ],
        ),
    ]
