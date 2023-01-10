# Standard library imports.

# Django imports.
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# First party imports.
from category.models import Category
from .models import Product, Variation
from cart.models import CartItem
from common.services import get_or_create_session_key
from .services import get_product_variations_data

def store(request, category_slug=None):

    category = None
    if category_slug:
        # Get products of specific category
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=category, is_available=True
        ).order_by("id")
    else:
        # Get all products
        products = Product.objects.all().filter(is_available=True).order_by("id")

    # Set paginator
    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    products_to_show = paginator.get_page(page)
    products_count = len(products_to_show.object_list)

    context = {
        "category": category,
        "products": products_to_show,
        "products_count": products_count,
    }
    return render(request, "store/store.html", context=context)


def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug, category=category)

    # Check if product is added to the cart
    is_added_to_cart = CartItem.objects.filter(
        product=product, cart__cart_id=get_or_create_session_key(request)
    ).exists()

    context = {
        "product": product,
        "is_added_to_cart": is_added_to_cart,
        "product_variations": get_product_variations_data(product)
    }

    return render(request, "store/product_details.html", context=context)


def search(request):

    # Get keyword from user or consider all
    keyword = request.GET.get("keyword", "")

    # Search by product name or category name
    products = (
        Product.objects.all()
        .order_by("-created_date")
        .select_related("category")
        .filter(Q(name__icontains=keyword) | Q(category__name__icontains=keyword) |
                Q(description__icontains=keyword) | Q(category__description__icontains=keyword))
    )

    # Set paginator
    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    products_to_show = paginator.get_page(page)
    products_count = len(products_to_show.object_list)

    context = {
        "products": products_to_show,
        "products_count": products_count,
    }
    return render(request, "store/store.html", context=context)
