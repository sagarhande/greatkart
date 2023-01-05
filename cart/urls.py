# Standard library imports.

# Django imports.
from django.urls import path

# First party imports.
from . import views


urlpatterns = [
      path("", views.cart, name="cart")
    ]