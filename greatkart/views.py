# Standard library imports.

# Django imports.
from django.shortcuts import render

# Third party imports.


def home(request):
    return render(request, template_name="home.html")