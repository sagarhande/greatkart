# Django imports
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# First party imports
from cart.models import CartItem

# Create your views here.


@login_required(login_url="login")
def place_order(request):
    user = request.user

    cart_items = CartItem.objects.filter(user=user)

    return render("")
