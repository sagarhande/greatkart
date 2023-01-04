# Standard library imports.

# Django imports.

# First party imports.
from category.models import Category


def menu_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)

