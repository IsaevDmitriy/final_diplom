from rest_framework import serializers
from backend.models import Shop, Product, ProductInfo, OrderItem, Order, Buyer, Category, User



class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'category',)


class ShopSerializer(serializers.ModelSerializer):
     class Meta:
        model = Shop
        fields = ('name', 'state', 'id')


class ShopStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('state',)


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    shop = serializers.StringRelatedField()

    class Meta:
        model = ProductInfo
        fields = ('id', 'product', 'shop', 'quantity', 'price',)


class BuyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Buyer
        fields = ('id', 'name', 'address', 'phone', 'user')


class OrderSerializer(serializers.ModelSerializer):
    buyer = BuyerSerializer()

    class Meta:
        model = Order
        fields = ('id', 'buyer', 'created_at', 'state')


class OrderItemSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product_info', 'quantity',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    contacts = BuyerSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'type', 'contacts')





