# Django imports
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required

# First party imports
from cart.models import CartItem
from .forms import OrderForm
from .models import Order

# Third party imports
import datetime

# Create your views here.


@login_required(login_url="login")
def place_order(request):
    user = request.user

    cart_items = CartItem.objects.filter(user=user)
    order_total, quantity = 0, 0
    for cart_item in cart_items:
        order_total += cart_item.sub_total()
        quantity += cart_item.quantity

    if request.method == "POST":
        form = OrderForm(request.POST)
        print("Form: ", form.is_valid())
        if form.is_valid():
            try:
                # Store form(billing info) into Order table
                obj = Order()
                obj.user = user
                obj.first_name = form.cleaned_data.get("first_name")
                obj.last_name = form.cleaned_data.get("last_name")
                obj.phone = form.cleaned_data.get("phone")
                obj.email = form.cleaned_data.get("email")
                obj.address_line1 = form.cleaned_data.get("address_line1")
                obj.address_line2 = form.cleaned_data.get("address_line2", "")
                obj.city = form.cleaned_data.get("city")
                obj.state = form.cleaned_data.get("state")
                obj.pin = form.cleaned_data.get("pin")
                
                obj.tax = round(order_total * 0.02, 2)
                obj.order_total = order_total + (order_total * 0.02)
                obj.ip = request.META.get("REMOTE_ADDR")
                obj.save()

                # Generate order number
                yr = int(datetime.date.today().strftime('%Y'))
                d = int(datetime.date.today().strftime('%d'))
                m = int(datetime.date.today().strftime('%m'))

                dt = datetime.date(yr, m, d)
                current_date = dt.strftime("%Y%m%d") 
                obj.order_number = current_date + str(obj.id)
                obj.save() 

                return redirect('checkout')
            except Exception as e:
                print("in Except ERROR: ", str(e))
                return redirect('checkout')
        
        else:
            return redirect('checkout')
