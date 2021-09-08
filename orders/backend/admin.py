from django.contrib import admin
from .models import Shop, OrderItem, Product, Order, User, Buyer, ProductInfo, ProductParameter, Category


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
        ...

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
        ...

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
        ...

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
        ...


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
        ...


@admin.register(User)
class ContactAdmin(admin.ModelAdmin):
        ...


@admin.register(Buyer)
class ProductAdmin(admin.ModelAdmin):
        ...


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
        ...


@admin.register(ProductParameter)
class ProductInfoAdmin(admin.ModelAdmin):
        ...
