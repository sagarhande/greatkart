from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class AccountAdmin(UserAdmin):
    # The fields to be used in displaying the User model in Admin panel.
    list_display = (
        'email', 'first_name', 'last_name', 'username', 'phone_number', 'last_login', 'date_joined',)
    # The fields need to be clickable
    list_display_links = ('email', 'first_name', 'last_name', 'username')
    # Readonly
    readonly_fields = ('last_login', 'date_joined')
    # Ordering
    ordering = ('-date_joined',)

    # Default
    list_filter = ()
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
