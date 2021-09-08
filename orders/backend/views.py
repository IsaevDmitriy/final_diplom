from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.models import Product, Shop, Category, ProductInfo, Order, OrderItem
from backend.serialaizers import ProductSerializer, ShopSerializer, ShopStatusSerializer, ProductInfoSerializer, OrderItemSerializer, OrderBasketSerializer
from rest_framework.status import HTTP_200_OK
from backend.permission import IsAuthorPermissions
from django_filters.rest_framework import DjangoFilterBackend
from backend.filters import ProductInfoFilter


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
        return Response(serializer.data, status=HTTP_200_OK)


class ShopStatusView(APIView):
    """Класс для просмотра/изменения статуса магазина"""
    permission_classes = [IsAuthorPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        queryset = Shop.objects.filter(user_id=request.user.id).select_related('user')
        serializer = ShopStatusSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)
        serializer = ShopStatusSerializer(data=request.data)
        if serializer.is_valid():
            Shop.objects.filter(user_id=request.user.id).select_related('user').update(**serializer.validated_data)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors)


class ProductInfoView(ListAPIView):
    """Класс для поиска товаров"""
    queryset = ProductInfo.objects.filter(shop__state='OPEN')
    serializer_class = ProductInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['shop', 'product', 'price', 'product__category']  # через ProductInfoFilter не работает?


class BasketView(APIView):
    """Класс для работы с корзиной пользователя"""
    permission_classes = [IsAuthorPermissions]

    """Добавить позицию в заказ"""
    def post(self, request, *args, **kwargs):
        items = request.data.get('goods')
        queryset = Order.objects.get_or_create(user_id=request.user.id, state='basket')
        basket = queryset[0]
        for item in items:
            item['order'] = basket.id
            serializer = OrderItemSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
        return JsonResponse({'Status': 'Позиции добавлены'})

    """Посмотреть заказ"""
    def get(self, request, *args, **kwargs):
        queryset = Order.objects.filter(user_id=request.user.id, state='basket')
        queryset_order = queryset[0]
        queryset_orderitem = OrderItem.objects.filter(order_id=queryset_order.id)
        total_price = 0
        for item in queryset_orderitem:
            total_price += item.quantity * item.product_info.price
        serializer = OrderBasketSerializer(queryset_orderitem, many=True)
        return JsonResponse({"id": queryset_order.id, "created_at": queryset_order.created_at, "state": queryset_order.state,
                             "buyer": queryset_order.buyer.name, "order_items": serializer.data, "total_price": total_price})












