# Standard library imports.

# Django imports.
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages,auth

# First party imports.
from .forms import RegistrationForm
from .models import Account


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
            messages.success(request,message="Registered successfully!!")
            
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


def logout(request):
    return 