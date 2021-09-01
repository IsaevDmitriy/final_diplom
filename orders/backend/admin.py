from django.contrib import admin
from .models import Shop, Category, Product, Order, User


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
        ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
        ...


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
        ...


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
        ...


@admin.register(User)
class ContactAdmin(admin.ModelAdmin):
        ...

