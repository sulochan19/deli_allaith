from django.contrib import admin
from .models import Order, Food, OrderContent, Cart

admin.site.register(Order)
admin.site.register(Food)
admin.site.register(OrderContent)
admin.site.register(Cart)