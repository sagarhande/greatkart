# Standard library imports.

# Django imports.
from django.contrib import admin

# First party imports.
from .models import Product

# Third party imports.


# To pre-populate slug field configure AdminProduct class
class AdminProduct(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'price', 'stock', 'is_available', 'category', 'modified_date')


admin.site.register(Product, AdminProduct)
