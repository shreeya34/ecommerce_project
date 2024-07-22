

# Register your models here.
from .models import *
from django.contrib import admin
from .models import Product, ProductImage, ProductOption,Review
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductOptionInline, ReviewInline]

admin.site.register(Product,ProductAdmin)
admin.site.register(Customer)
# admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Review)

