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
    return email.send()



def send_password_reset_email(request, user, email):
    """ 
    Send reset password email to user email 
    """
    site = get_current_site(request)
    mail_sub = "GreatKart account password request"
    message = render_to_string('accounts/email_reset_password_template.html', context= {
               'user': user,
               'domain': site,
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': default_token_generator.make_token(user),
           })

    to_email = email
    email = EmailMessage(mail_sub, message, to=[to_email])
    return email.send()


def merge_cart_items(curr, existing):
    final_cart_items = [list(existing)]
    existing_dict = {}
    incoming_dict = {}
    product_variations = []
    for i in existing:
        existing_dict[i.product.id] = existing_dict.get(i.product.name, []).append(i)
    
    for i in curr:
        incoming_dict[i.product.id] = incoming_dict.get(i.product.name, []).append(i)
        product_variations.append(list(i.product_variation.all()))

    for pid in incoming_dict.keys():   # incoming product id's
        if pid in existing_dict.keys():
            product_variations = [i.product_variation for i in  incoming_dict.get(pid)]
            matched_items_from_existing = existing_dict.get(pid) 
            
            existing_variations = {} 
            for item in matched_items_from_existing:
                existing_variations[item] = set(item.product_variation.all())
                
            is_exist = False
            for key, value in existing_variations.items():
                if set(product_variations) == value:
                    is_exist= True
                    existing_item = key
            if is_exist:
                # increase quantity
                existing_item.quantity += 1
                existing_item.save()
        else:
            final_cart_items.append(incoming_dict.get(pid))

