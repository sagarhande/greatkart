# Django imports
from django.contrib import admin
from .models import Account, AccountProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

# Register your models here.


class AccountAdmin(UserAdmin):
    # The fields to be used in displaying the User model in Admin panel.
    list_display = (
        "email",
        "first_name",
        "last_name",
        "username",
        "phone_number",
        "last_login",
        "date_joined",
    )
    # The fields need to be clickable
    list_display_links = ("email", "first_name", "last_name", "username")
    # Readonly
    readonly_fields = ("last_login", "date_joined")
    # Ordering
    ordering = ("-date_joined",)

    # Default
    list_filter = ()
    filter_horizontal = ()
    fieldsets = ()


class AccountProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(
            '<img src="{}" width="30" height="30" style="border-radius:50%;">'.format(
                object.profile_picture.url
            )
        )

    thumbnail.short_description = "Profile Picture"
    list_display = ("thumbnail", "user", "city", "state", "country")
    list_display_links = ("user", "thumbnail")


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountProfile, AccountProfileAdmin)
