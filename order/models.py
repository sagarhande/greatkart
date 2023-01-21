# Standard library imports.

# Django imports.
from django.db import models

# First party imports.
from accounts.models import Account
from store.models import Product, Variation


class Payment(models.Model):

    COD = "COD"
    NB = "NB"
    PAYPAL = "PAYPAL"

    payment_method_choices = ((COD, "COD"), (NB, "Net Banking"), (PAYPAL, "PAYPAL"))

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    method = models.CharField(
        max_length=50, choices=payment_method_choices, default=PAYPAL
    )
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.payment_id


class Order(models.Model):

    STATUS = (
        ("NEW", "NEW"),
        ("ACCEPTED", "ACCEPTED"),
        ("COMPLETED", "COMPLETED"),
        ("CANCELLED", "CANCELLED"),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    order_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    email = models.CharField(max_length=50)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default="NEW")
    ip = models.CharField(max_length=20, blank=True, null=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.order_number
    
    def full_name(self):
        return self.first_name + " " + self.last_name
    
    def full_address(self):
        return self.address_line1 + ", " + self.address_line2

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variation = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product.name
