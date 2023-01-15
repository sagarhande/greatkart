# Standard library imports.

# Django imports.
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# First party imports.
from store.models import Product, Variation
from cart.models import Cart, CartItem
from common.services import get_or_create_session_key, get_session_key


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
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

        # Main logic for product cart addition
        # Add product_variation to cart
        try:
           
            cart = Cart.objects.get(cart_id=get_session_key(request))  # We storing session key as a cart id

        except Cart.DoesNotExist :
            cart = Cart.objects.create(
                cart_id=get_or_create_session_key(request)
                )
            cart.save()

        # Add cart item
        cart_items = CartItem.objects.filter(product = product, cart=cart)

        if cart_items.exists() :

            """
            incoming --> [v1,v2]
            in DB    --> [[v1,v2], [v3,v4]]

            """
            existing_variations = {} 
            for item in cart_items:
                existing_variations[item] = set(item.product_variation.all())

            is_exist = False
            for key, value in existing_variations.items():
                if set(product_variations) == value:
                    is_exist= True
                    item = key

            if is_exist:
                # increase quantity
                item.quantity += 1
                item.save()

            else:
                # craete new one
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

        else:
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


def remove_from_cart(request, cart_item_id):

    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.quantity = cart_item.quantity - 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
    except CartItem.DoesNotExist:
        raise Exception("cart item does not exist")

    return redirect('cart')


def discard_from_cart(request, cart_item_id):
    try:
        CartItem.objects.get(id=cart_item_id).delete()
    except CartItem.DoesNotExist:
        raise Exception("cart item does not exist")

    return redirect('cart')

@login_required(login_url="login")
def checkout(request, total=0, quantity=0, cart_items=None):
    if request.method == "POST":
        pass

    else:

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
        return render(request, "store/checkout.html", context=context)





