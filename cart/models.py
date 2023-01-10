# Standard library imports.

# Django imports.
from django.db import models
# First party imports.
from accounts.models import Account
from store.models import Product, Variation


class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True, null=True)
    # account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variation = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product

    def sub_total(self):
        return self.product.price*self.quantity
