# Standard library imports.

# Django imports.
from django.contrib import admin

# First party imports.
from .models import *

# Third party imports.


# To pre-populate slug field configure AdminProduct class
class AdminProduct(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'price', 'stock', 'is_available', 'category', 'modified_date')

# Admin settings for Variation model
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category', 'variation_value')
            

admin.site.register(Product, AdminProduct)
admin.site.register(Variation, VariationAdmin)