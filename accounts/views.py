# Standard library imports.

# Django imports.
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
# First party imports.
from .forms import RegistrationForm
from .models import Account
from .services import send_activation_email


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

            user = Account.objects.create_user(first_name=first_name,
                                               last_name=last_name, 
                                               username=username,
                                               email=email,
                                               phone_number=phone_number,
                                               password=password
                                                )

            is_email_sent = send_activation_email(request, user, email)
            if is_email_sent:
                return redirect(f'accounts/login/?command=verification&email={email}')
            else:
                messages.error(request,message="something went wrong!!")
            
    else:
        form = RegistrationForm()


    context = {
        "form": form,
    }
    return render(request, 'accounts/register.html', context=context)


def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")           # This is coming from name attr of input tag
        password = request.POST.get("password")     # eg- <input type="email" class="form-control" name="email" >

        user = auth.authenticate(email=email, password=password)
        print("HERE: ", user, email, password)
        if user:
            auth.login(request, user)
            messages.success(request, "login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials!")
            return redirect('login')

    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):

    auth.logout(request)
    messages.success(request, "Logout successfully!")
    return redirect('login') 


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
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link!")
        return redirect('register')