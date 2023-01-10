# Standard library imports.

# Django imports.
from django.db import models
# First party imports.

# Third party imports.


class VariationManager(models.Manager):
    
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)