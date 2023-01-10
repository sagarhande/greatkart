# Standard library imports.

# Django imports.

# First party imports.
from .models import Variation


def get_product_variations_data(product):
        # Get Variation data of product in dict format
    """
    data = {
        "c1": [v1, v2],
        "c2": [v1, v2]
    }
    """

    if not product:
        return {}

    data = {}
    for variation_category in Variation.variation_category_choice:
        data[variation_category[0]] = []
    
    # Get all variations of product
    for obj in Variation.objects.filter(product=product, is_active=True):
        data[obj.variation_category].append(obj.variation_value)
    
    return data
    




