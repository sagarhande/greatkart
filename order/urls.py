# Standard library imports.

# Django imports.
from django.urls import path

# First party imports.
from . import views


urlpatterns = [
    path("place-order/", views.place_order, name="place-order"),
    path("payments/", views.payments, name="payments"),
    path("order-successful/", views.order_successful, name="order-successful"),

]
