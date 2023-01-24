# Standard library imports.

# Django imports.
from django import forms

# First party imports.
from .models import Account, AccountProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "password", "phone_number"]

    def __init__(self, *args, **kwargs):
        # This is to initialise all from fields with css class "form-control"
        field_placeholder_map = {
            "first_name": "Enter first name",
            "last_name": "Enter last name",
            "email": "Enter email",
            "phone_number": "Enter phone number",
            "password": "Enter password",
            "confirm_password": "Re-enter password",
        }
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].widget.attrs["placeholder"] = field_placeholder_map.get(
                field, ""
            )

    def clean(self):
        cleand_data = super(RegistrationForm, self).clean()
        password = cleand_data.get("password")
        confirm_password = cleand_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password doesn't match!!")


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("first_name", "last_name", "phone_number")

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class AccountProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        error_messages={"invalid": "image files only"},
        widget=forms.FileInput,
    )

    class Meta:
        model = AccountProfile
        fields = (
            "address_line1",
            "address_line2",
            "profile_picture",
            "city",
            "state",
            "country",
        )

    def __init__(self, *args, **kwargs):
        super(AccountProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
