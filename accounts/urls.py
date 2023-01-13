# Standard library imports.

# Django imports.
from django.urls import path

# First party imports.
from . import views


urlpatterns = [
      path("register/", views.register, name="register"),
      path("login/", views.login, name="login"),
      path("logout/", views.logout, name="logout"),
      path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    ]