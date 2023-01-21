# Django imports
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# First party imports
from cart.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from .services import *

# Third party imports
import datetime
import json

# Create your views here.


@login_required(login_url="login")
def place_order(request):
    user = request.user

    cart_items = CartItem.objects.filter(user=user)
    order_total, quantity = 0, 0
    for cart_item in cart_items:
        order_total += cart_item.sub_total()
        quantity += cart_item.quantity
    tax = round(order_total * 0.02, 2)
    grand_total = order_total + tax


    if request.method == "POST":
        form = OrderForm(request.POST)
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
                
                obj.tax = tax
                obj.order_total = grand_total
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

                context = {
                    'order': obj,
                    'cart_items': cart_items,
                    'tax': tax,
                    'total': order_total,
                    'grand_total': grand_total,

                }

                return render(request, "orders/payments.html", context)
            except Exception as e:
                print(f"\nException While saving order details: {e}\n")
                return redirect('checkout')
        
        else:
            return redirect('checkout')


def payments(request):
    try:
        body = json.loads(request.body)
        order = Order.objects.get(user=request.user, order_number=body.get("orderID"), is_ordered=False)

        # Store transaction details in Payment model
        payment = Payment(
            user = request.user,
            payment_id = body.get("transID"),
            status = body.get("status"),
            method = body.get("payment_method"),
            amount_paid = str(order.order_total),
        )
        payment.save()
        # Change in Order
        order.payment = payment
        order.is_ordered = True
        order.status = body.get("status")
        order.save()


        # Move cart items to OderProduct table
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        
        for item in cart_items:
            ordered_product = OrderProduct(
                order = order,
                payment = payment,
                user = request.user,
                product = item.product, 
                quantity = item.quantity,
                is_ordered = True,
            )
            ordered_product.save()
            # NOTE: while creating obj, ManyToMany field cann't be added, it should be added after save()
            ordered_product.product_variation.set(item.product_variation.all())
            # for variation in item.product_variation.all():
            #     ordered_product.product_variation.add(variation) 
            ordered_product.save()

    
            # Reduce product quantity
            product = item.product
            product.stock -= item.quantity
            product.save()

        # Clear Cart
        cart_items.delete()

        # Send order recieved email to customer
        send = send_order_recived_email(request, order)
        if not send:
            print("Error while sending a `order recived email`")
            pass         

        # Send order number and transaction ID back to user
        data = {
            'order_number': order.order_number,
            'payment_id': payment.payment_id
        }
        return JsonResponse(data)


    except Exception as e:
        print(f"\nException While saving transaction details: {e}\n")
        return JsonResponse({"Error": f"{e}"})




def order_successful(request):
    try:
        order_number = request.GET.get("order_number")
        payment_id = request.GET.get("payment_id")

        order = Order.objects.get(order_number=order_number, is_ordered=True)
        payment = Payment.objects.get(payment_id=payment_id)
        ordered_items = OrderProduct.objects.filter(order = order, payment = payment,  is_ordered = True,)
        context = {
            'order': order,
            'payment': payment,
            'ordered_items': ordered_items,
            'sub_total': order.order_total - order.tax
        }
        return render(request, "orders/order_successful.html", context=context)
    except Exception as e:
        print(f"Exception occure while rendering order_successful.html\n Error: {e}")
        return render(request, "orders/order_successful.html")
