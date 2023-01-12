# Standard library imports.

# Django imports.
from django.shortcuts import render

# First party imports.
from .forms import RegistrationForm



def register(request):
    form = RegistrationForm()
    context = {
        "form": form,
    }
    return render(request, 'accounts/register.html', context=context)


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return 