# Standard library imports.

# Django imports.
from django.urls import path

# First party imports.
from . import views


urlpatterns = [
      path("", views.cart, name="cart"),
      path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
      path("remove_from_cart/<int:cart_item_id>/", views.remove_from_cart, name="remove_from_cart"),
      path("discard_from_cart/<int:cart_item_id>/", views.discard_from_cart, name="discard_from_cart"),
    ]