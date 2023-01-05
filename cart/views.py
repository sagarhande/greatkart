# Standard library imports.

# Django imports.
from django.shortcuts import render, HttpResponse

# First party imports.


def cart(request):
    return render(request, "store/cart.html")
