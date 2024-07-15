from django.contrib import admin

# Register your models here.
from .models import *
from .models import Product



admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Color)
admin.site.register(Size)