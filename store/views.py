# Standard library imports.

# Django imports.
from django.shortcuts import render, get_object_or_404

# First party imports.
from category.models import Category
from .models import Product


def store(request, category_slug=None):

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)

    products_count = products.count()

    context = {
        'category': category,
        'products': products,
        'products_count': products_count,
        }
    return render(request, 'store/store.html', context=context)
