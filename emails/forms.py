from django import forms
from .models import Email


class EmailForm(forms.ModelForm):
    # replicates the  form from the admin dashboard's model
    class Meta:
        model = Email
        # displays all fields on the
        fields = ('__all__')
