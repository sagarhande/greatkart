# Standard library imports.

# Django imports.
from django.db import models
from django.urls import reverse
from django.db.models import Avg, Count

# First party imports.
from category.models import Category
from .managers import *
from accounts.models import Account

# Third party imports.


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to="photos/products")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse("product_detail", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = ReviewRating.objects.filter(product=self, is_active=True).aggregate(
            average=Avg("rating")
        )
        avg = 0
        if reviews["average"]:
            avg = float(reviews["average"])
        return avg

    def review_count(self):
        reviews = ReviewRating.objects.filter(product=self, is_active=True).aggregate(
            count=Count("id")
        )
        count = 0
        if reviews["count"]:
            count = float(reviews["count"])
        return int(count)


class Variation(models.Model):
    variation_category_choice = (
        ("color", "color"),
        ("size", "size"),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choice
    )
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    variation_category_list = ["color", "size"]

    def __str__(self) -> str:
        return self.variation_category + " : " + self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="store/products", max_length=255)

    def __str__(self) -> str:
        return self.product.name
