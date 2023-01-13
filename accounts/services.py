# Standard library imports.

# Django imports.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# First party imports.



def send_activation_email(request, user, email):
    """  ###### IMPORTANT ###### 
   
    According to Google's new sign-in policy, you need to create 
    App Password to send emails from your application. So create 
    App Password by following this article https://support.google.com/accounts/answer/185833 
    and set that 16-digit app password to EMAIL_HOST_PASSWORD in your settings.py.
    """
    
    site = get_current_site(request)
    mail_sub = "Activate your Greatkart account!"
    message = render_to_string('accounts/email_varification_template.html', context= {
               'user': user,
               'domain': site,
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': default_token_generator.make_token(user),
           })

    to_email = email
    email = EmailMessage(mail_sub, message, to=[to_email])
    print(vars(email))
    return email.send()