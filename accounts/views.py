# Standard library imports.

# Django imports.
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# First party imports.
from .forms import RegistrationForm
from .models import Account
from .services import send_activation_email, send_password_reset_email, merge_cart_items
from cart.models import Cart, CartItem
from common.services import get_session_key, get_or_create_session_key
from store.models import Product

# Third party imports
import requests


def register(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            phone_number = form.cleaned_data.get("phone_number")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                phone_number=phone_number,
                password=password,
            )

            is_email_sent = send_activation_email(request, user, email)
            if is_email_sent:
                return redirect(f"accounts/login/?command=verification&email={email}")
            else:
                messages.error(
                    request,
                    message="something went wrong while sending activation email!!",
                )

    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context=context)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")  # This is coming from name attr of input tag
        password = request.POST.get(
            "password"
        )  # eg- <input type="email" class="form-control" name="email" >

        user = auth.authenticate(email=email, password=password)
        if user:
            try:
                # Incoming
                cart = Cart.objects.filter(cart_id=get_session_key(request))[:1]
                cart_items = CartItem.objects.filter(cart=cart)

                # Existing
                ex_cart_items = CartItem.objects.filter(user=user)

                # check incoming present in Existing
                for new_item in cart_items:
                    is_present = False
                    for ex_item in ex_cart_items:
                        if new_item.product == ex_item.product and set(
                            new_item.product_variation.all()
                        ) == set(ex_item.product_variation.all()):
                            # increse quantity of existing item
                            ex_item.quantity += 1
                            ex_item.save()

                            # delete new item
                            new_item.delete()
                            is_present = True
                            break

                    if not is_present:
                        # assign a current user
                        new_item.user = user
                        new_item.cart = ex_item.cart if ex_item else None
                        new_item.save()

            except Exception as e:
                print("\n ERROR: ", str(e))
                pass

            auth.login(request, user)
            url = request.META.get("HTTP_REFERER")
            try:
                next_page = "home"
                query = requests.utils.urlparse(url).query  # next=/cart/checkout
                if query:
                    params = dict(x.split("=") for x in query.split("&"))
                    if "next" in params:
                        next_page = "cart"
                        # next_page = params["next"]

                return redirect(next_page)

            except:
                return redirect("home")

        else:
            messages.error(request, "Invalid login credentials!")
            return redirect("login")

    return render(request, "accounts/login.html")


@login_required(login_url="login")
def logout(request):

    auth.logout(request)
    messages.success(request, "Logout successfully!")
    return redirect("login")


def activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except (TypeError, ValueError, Account.DoesNotExist, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Congratulations! your account is now activated.")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation link!")
        return redirect("register")


@login_required(login_url="login")
def dashboard(request):
    return render(request, "accounts/dashboard.html")


def forgot_password(request):

    if request.method == "POST":
        try:
            email = request.POST.get("email")
            user = Account.objects.get(email__exact=email)
            if user:
                is_email_sent = send_password_reset_email(request, user, email)

                if is_email_sent:
                    messages.success(
                        request, f"Password reset mail has been sent to : {email}"
                    )
                    return redirect("login")

                else:
                    messages.error(
                        request,
                        message="something went wrong while sending password reset email!!",
                    )
                    return redirect("forgot-password")

        except Account.DoesNotExist as err:
            messages.error(request, "no account found with give email address!")
            return redirect("forgot-password")

    return render(request, "accounts/forgot_password.html")


def reset_password_validate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except (TypeError, ValueError, Account.DoesNotExist, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please request your password")
        return redirect("reset-password")

    else:
        messages.error(request, "Activation link has expired.")
        return redirect("login")


def reset_password(request):
    if request.method == "POST":
        password = request.POST.get(
            "password"
        )  # This is coming from name attr of input tag
        confirm_password = request.POST.get(
            "confirm_password"
        )  # eg- <input type="email" class="form-control" name="email" >

        if password != confirm_password:
            messages.error(request, "passwords does not match!")
            return redirect("reset-password")

        uid = request.session.get("uid")
        user = Account.objects.get(pk=uid)
        user.set_password(password)
        user.save()
        messages.success(request, "Password reseted successfully, please login now.")
        return redirect("login")
    return render(request, "accounts/reset_password.html")
