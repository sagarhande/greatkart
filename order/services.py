# Standard library imports.

# Django imports.
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# First party imports.


def send_order_recived_email(request, order):
    """  ###### IMPORTANT ###### 
    According to Google's new sign-in policy, you need to create 
    App Password to send emails from your application. So create 
    App Password by following this article https://support.google.com/accounts/answer/185833 
    and set that 16-digit app password to EMAIL_HOST_PASSWORD in your settings.py.
    """

    mail_sub = "We have received your order!"
    message = render_to_string('orders/order_received_email.html', context= {
               'user': request.user,
               'order': order
           })

    to_email = request.user.email
    email = EmailMessage(mail_sub, message, to=[to_email])
    return email.send()
