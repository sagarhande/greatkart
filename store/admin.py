# Standard library imports.

# Django imports.
from django.contrib import admin

# First party imports.
from .models import *

# Third party imports.
import admin_thumbnails


@admin_thumbnails.thumbnail("image")
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 0
    readonly_fields = ("product", "image")


class ReviewRatingInline(admin.TabularInline):
    model = ReviewRating
    extra = 0
    readonly_fields = (
        "product",
        "user",
    )
    fields = ("rating", "user", "subject", "is_active")


# To pre-populate slug field configure AdminProduct class
class AdminProduct(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "name",
        "price",
        "stock",
        "is_available",
        "category",
        "modified_date",
    )
    inlines = (ReviewRatingInline, ProductGalleryInline)


# Admin settings for Variation model
class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "variation_category", "variation_value", "is_active")
    list_editable = ("is_active",)
    list_filter = ("product", "variation_category", "variation_value")


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ("product", "rating", "user", "subject", "is_active", "created_at")
    list_editable = ("rating", "subject", "is_active")


admin.site.register(Product, AdminProduct)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ProductGallery)
