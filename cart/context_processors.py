# Standard library imports.

# Django imports.

# First party imports.
from cart.models import Cart, CartItem
from common.services import get_session_key


def total_items_in_cart(request):
    count = 0
    if 'admin' in request.path:
        # Don't do anything for Admin user
        return {}
    try:
        cart = Cart.objects.get(cart_id=get_session_key(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            count += item.quantity
    except Cart.DoesNotExist:
        count = 0
    return dict(total_items_in_cart=count)

