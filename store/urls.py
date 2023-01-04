# Standard library imports.

# Django imports.
from django.urls import path

# First party imports.
from . import views


urlpatterns = [
        path('', views.store, name='store'),
        path('<slug:category_slug>/', views.store, name='products_by_category'),
    ]