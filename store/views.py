# Standard library imports.

# Django imports.
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages

# First party imports.
from order.models import OrderProduct
from category.models import Category
from .models import Product, ReviewRating
from cart.models import CartItem
from .forms import ReviewForm
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

    try:
        is_ordered_previously = OrderProduct.objects.filter(user__id = request.user.id, product=product, is_ordered=True).exists()            
    except OrderProduct.DoesNotExist:
        is_ordered_previously = None

    context = {
        "product": product,
        "is_added_to_cart": is_added_to_cart,
        "product_variations": get_product_variations_data(product),
        "is_ordered_previously": is_ordered_previously,
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


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST,instance=review)
            form.save()
            messages.success(request, "Thank you, your review has been updated!")
            return  redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                obj = ReviewRating(
                    subject = form.cleaned_data.get("subject"),
                    rating = form.cleaned_data.get("rating"),
                    review = form.cleaned_data.get("review"),
                    ip = request.META.get('REMOTE_ADDR'),
                    product_id = product_id,
                    user = request.user,
                )

                obj.save()
                messages.success(request, "Thank you, your review has been submitted!")

            return redirect(url)

