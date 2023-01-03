# Standard library imports.

# Django imports.
from django.shortcuts import render

# First party imports.
from category.models import Category


def store(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        }
    return render(request, 'store/store.html', context=context)
