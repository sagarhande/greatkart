# Standard library imports.

# Django imports.
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist

# First party imports.
from store.models import Product
from cart.models import Cart, CartItem
from common.services import get_or_create_session_key, get_session_key


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=get_session_key(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.sub_total())
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": round(total*0.02, 2),   # 2% tax on total
        "grand_total": total+(total*0.02),
        }
    return render(request, "store/cart.html", context=context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        # We storing session key as a cart id
        cart = Cart.objects.get(cart_id=get_session_key(request))

    except Cart.DoesNotExist :
        cart = Cart.objects.create(
            cart_id=get_or_create_session_key(request)
            )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product = product, cart=cart)
        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1,
            is_active=True
            )
        cart_item.save()

    return redirect('cart')


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        # We storing session key as a cart id
        cart = Cart.objects.get(cart_id=get_session_key(request))
    except Cart.DoesNotExist:
        raise Exception("cart not present")

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity = cart_item.quantity - 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
    except CartItem.DoesNotExist:
        raise Exception("cart item does not exist")

    return redirect('cart')


def discard_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product, cart__cart_id=get_session_key(request))
        cart_item.delete()
    except CartItem.DoesNotExist:
        raise Exception("cart item does not exist")

    return redirect('cart')






