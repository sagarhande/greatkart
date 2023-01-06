# Standard library imports.

# Django imports.
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# First party imports.
from category.models import Category
from .models import Product
from cart.models import CartItem
from common.services import get_or_create_session_key


def store(request, category_slug=None):

    category = None
    if category_slug:
        # Get products of specific category
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        # Get all products
        products = Product.objects.all().filter(is_available=True)

    # Set paginator
    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    product_to_show = paginator.get_page(page)
    products_count = len(product_to_show.object_list)

    context = {
        'category': category,
        'products': product_to_show,
        'products_count': products_count,
        }
    return render(request, 'store/store.html', context=context)


def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug, category=category)

    # Check if product is added to the cart
    cart_item = CartItem.objects.filter(product=product, cart__cart_id=get_or_create_session_key(request)).exists()

    context = {
         "product": product,
         "is_added": cart_item,
        }

    return render(request, 'store/product_details.html', context=context)
