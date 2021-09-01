from rest_framework import serializers
from orders.backend.models import Shop, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'product', 'shop', 'quantity', 'price',)


class ShopSerializer(serializers.ModelSerializer):
     class Meta:
        model = Shop
        fields = ('id', 'name', 'url', 'state',)
