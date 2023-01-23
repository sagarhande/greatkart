# Standard library imports.

# Django imports.
from django import forms

# First party imports.
from .models import *

# Third party imports.


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ('subject', 'review', 'rating')