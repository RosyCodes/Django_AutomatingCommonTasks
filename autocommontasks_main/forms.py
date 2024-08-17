from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# uses the Django User Form


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email Address')
    first_name = forms.CharField(required=True, label='First Name')
    last_name = forms.CharField(required=True, label='Last Name')

    class Meta:
        model = User
        #  the mmodel fields we need to display on our form
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')
