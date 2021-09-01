from rest_framework.response import Response
from rest_framework.views import APIView
from orders.backend.models import Product, Shop, Category
from orders.backend.serialaizers import ProductSerializer, ShopSerializer


class ProductView(APIView):
    """Класс для просмотра списка товаров"""

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)





class ShopView(APIView):
    """Класс для просмотра списка магазинов"""

    def get(self, request, *args, **kwargs):
        queryset = Shop.objects.all()
        serializer = ShopSerializer(queryset, many=True)
        return Response(serializer.data)
