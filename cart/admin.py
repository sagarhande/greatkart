# Standard library imports.

# Django imports.
from django.contrib import admin
# First party imports.
from .models import Cart, CartItem

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)