from rest_framework import serializers
from backend.models import Shop, Product, ProductInfo, OrderItem, Order



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name',)


class ShopSerializer(serializers.ModelSerializer):
     class Meta:
        model = Shop
        fields = ('name', 'state',)


class ShopStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('state',)



class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    shop = ShopSerializer()
    class Meta:
        model = ProductInfo
        fields = ('product', 'shop', 'quantity', 'price',)



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'quantity', 'order',)



class OrderBasketSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer()

    class Meta:
        model = OrderItem
        fields = ('product_info', 'quantity',)









