# Standard library imports.

# Django imports.
from django import forms

# First party imports.
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password',
        # 'class' : 'form-control'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password again',
        # 'class' : 'form-control'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_number']
    
    def __init__(self, *args, **kwargs):
        # This is to initialise all from fields with css class "form-control"
        field_placeholder_map = {
            'first_name': "Enter first name",
            'last_name': "Enter last name",
            'email': "Enter email",
            'phone_number': "Enter phone number",
            'password': "Enter password",
            'confirm_password': "Re-enter password"
           
        }
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = field_placeholder_map.get(field, "")
