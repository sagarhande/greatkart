# Standard library imports.

# Django imports.
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist

# First party imports.
from store.models import Product, Variation
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
    product_variations = []

    if request.method == 'POST':
        for key in request.POST:
            
            # Check for valid variation category
            if key not in Variation.variation_category_list:
                continue

            value = request.POST.get(key)      # Coming from select tab in from eg. <select name="color" class="form-control">
            
            try:
                variation =  Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
            except:
                variation = Variation.objects.create(
                    product=product,
                     variation_category=key,
                     variation_value=value,
                     is_active=True,
                )
            
            product_variations.append(variation)

        # Get or Create Cart
        try:
           
            cart = Cart.objects.get(cart_id=get_session_key(request))  # We storing session key as a cart id

        except Cart.DoesNotExist :
            cart = Cart.objects.create(
                cart_id=get_or_create_session_key(request)
                )
            cart.save()

        # Add cart item
        try:
            cart_item = CartItem.objects.get(product = product, cart=cart)
            if len(product_variations) > 0:
                for item in product_variations:
                    cart_item.product_variation.add(item)  # As this is many to many relationship
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1,
                is_active=True
                )
            if len(product_variations) > 0:
                for item in product_variations:
                    cart_item.product_variation.add(item)
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






