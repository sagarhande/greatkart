from django.contrib import admin
from .models import Payment, Order, OrderProduct

# Register your models here.

# To pre-populate slug field configure AdminProduct class
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'method', 'amount_paid', 'status', 'created_at')

# Admin settings for Variation model
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number','user', 'order_total', 'status', 'is_ordered', 'created_at')
    list_editable = ('is_ordered', 'status')
    list_filter = ('status', 'is_ordered')
    search_fields = ('order_number',)

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
