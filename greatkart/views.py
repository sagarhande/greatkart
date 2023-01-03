# Standard library imports.

# Django imports.
from django.shortcuts import render

# First party imports.
from store.models import Product

# Third party imports.


def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        "products": products,
        }
    return render(request, template_name='home.html', context=context)
