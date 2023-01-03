# Standard library imports.

# Django imports.
from django.contrib import admin
# First party imports.
from .models import Category


# To pre-populate slug field configure CategoryAdmin class
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'description')


admin.site.register(Category, CategoryAdmin)

