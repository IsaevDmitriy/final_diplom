import requests
import yaml
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from backend.models import Product, Shop, Category, ProductInfo, Order, OrderItem, Buyer, ProductParameter, Parameter
from backend.serialaizers import ProductSerializer, ShopSerializer, ShopStatusSerializer, ProductInfoSerializer, \
    OrderItemSerializer, BuyerSerializer, CategorySerializer, OrderSerializer, UserSerializer
from backend.permission import IsAuthorPermissions, IsShopPermissions



class RegisterAccountView(APIView):
    """Класс для регистрации"""

    def post(self, request, *args, **kwargs):
        if {'username', 'password'}.issubset(request.data):
                request.data._mutable = True
                request.data.update({})
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    user.set_password(request.data['password'])
                    user.save()
                    return JsonResponse({'Status': True})
                else:
                    return JsonResponse({'Status': False, 'Errors': user_serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class TokenAccountView(APIView):
    """Класс для получения токена"""

    def post(self, request, *args, **kwargs):
        if {'username', 'password'}.issubset(request.data):
            user = authenticate(request, username=request.data['username'], password=request.data['password'])
            if user is not None:
                if user.is_active:
                    token = Token.objects.get_or_create(user=user)[0]
                    return JsonResponse({'Status': True, 'Token': token.key})

            return JsonResponse({'Status': False, 'Errors': 'Не удалось авторизовать'})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class AccountDetailsView(APIView):
    """Класс для работы c данными пользователя"""
    permission_classes = [IsAuthorPermissions]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if 'password' in request.data:
            request.user.set_password(request.data['password'])
        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'Status': True})
        else:
            return JsonResponse({'Status': False, 'Errors': user_serializer.errors})


class BuyerView(APIView):
    """Класс для работы с контактами пользователя"""
    permission_classes = [IsAuthorPermissions]

    """Посмотреть профиль покупателя"""
    def get(self, request, *args, **kwargs):
        contact = Buyer.objects.filter(
            user_id=request.user.id)
        serializer = BuyerSerializer(contact, many=True)
        return Response(serializer.data)

    """Добавить новый адрес (контакт)"""
    def post(self, request, *args, **kwargs):
        if type(request.data.get('address')) == str and type(request.data.get('phone')) == str \
                and type(request.data.get('name')) == str:
            request.data._mutable = True
            request.data.update({'user': request.user.id})
            serializer = BuyerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'Status': True, 'item': serializer.data})
            else:
                return JsonResponse({'Status': False, 'Errors': serializer.errors})
        else:
            return JsonResponse({'Status': False, 'Error': 'Не указаны все необходимые аргументы'})

    """Удалить адрес (контакт)"""
    def delete(self, request, *args, **kwargs):
        items = request.data.get('items')
        if items:
            items = items.split(',')
            for item_id in items:
                if item_id.isdigit():
                    try:
                        Buyer.objects.filter(id=item_id).delete()[0]
                    except:
                        return JsonResponse({'Status': False, 'Error': 'Ошибка удаления из БД'})
                else:
                    return JsonResponse({'Status': False, 'Error': 'Введите корректный номер заказа'}, status=403)
            return JsonResponse({'Status': 'Адрес(а) удалены'})
        else:
            return JsonResponse({'Status': False, 'Error': 'Не указаны все необходимые данные'}, status=403)

    """Изменить адрес (контакт)"""
    def put(self, request, *args, **kwargs):
        if type(request.data.get('id')) == int:
            if 'name' in request.data or 'phone' in request.data or 'address' in request.data:
                try:
                    Buyer.objects.filter(id=request.data['id'], user_id=request.user.id).update(**request.data)
                except:
                    return JsonResponse({'Status': False, 'Error': 'Ошибка записи в БД'})
                else:
                    return JsonResponse({'Status': True, 'items': request.data})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые данные'})





class CategoryView(APIView):
    """Класс для просмотра списка категорий"""

    def get(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class ProductView(APIView):
    """Класс для просмотра списка товаров"""

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ShopView(APIView):
    """Класс для просмотра списка магазинов"""

    def get(self, request, *args, **kwargs):
        queryset = Shop.objects.filter(state='OPEN')
        serializer = ShopSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductInfoView(ListAPIView):
    """Класс для поиска товаров"""
    queryset = ProductInfo.objects.filter(shop__state='OPEN').select_related(
            'shop', 'product__category').distinct()
    serializer_class = ProductInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['shop', 'product__category']


class BasketView(APIView):
    """Класс для работы с корзиной пользователя"""
    permission_classes = [IsAuthorPermissions]

    """Добавить позицию в заказ"""
    def post(self, request, *args, **kwargs):
        items = request.data.get('items')
        if items:
            basket = Order.objects.get_or_create(user_id=request.user.id, state='basket')[0]
            for item in items:
                if type(item['product_info']) == int and type(item['quantity']) == int:
                    try:
                        OrderItem.objects.create(order_id=basket.id, product_info_id=item['product_info'],
                                                 quantity=item['quantity'])
                    except:
                        return JsonResponse({'Status': False, 'Error': 'Ошибка записи в БД'})

                else:
                    return JsonResponse({'Status': False, 'Error': 'Не указаны все необходимые данные'}, status=403)
            return JsonResponse({'Status': 'Позиция(и) добавлены'})
        else:
            return JsonResponse({'Status': False, 'Error': 'Не указаны все необходимые данные'}, status=403)


    """Посмотреть цену заказа"""
    def get(self, request, *args, **kwargs):
        queryset = Order.objects.filter(user_id=request.user.id, state='basket').distinct()
        if queryset:
            basket = queryset[0]
            order_items = OrderItem.objects.filter(order_id=basket.id).distinct()
            if order_items:
                total_price = 0
                for item in order_items:
                    total_price += item.quantity * item.product_info.price
                serializer = OrderItemSerializer(order_items, many=True)
                return JsonResponse({'items': serializer.data, 'total_price': total_price})
            else:
                return JsonResponse({'Status': False, 'Error': 'Добавьте позиции в заказ'}, status=403)
        else:
            return JsonResponse({'Status': False, 'Error': 'Нет открытых заказов'}, status=403)


    """Удалить позицию из заказа"""
    def delete(self, request, *args, **kwargs):
        items = request.data.get('items')
        queryset = Order.objects.get(user_id=request.user.id, state='basket')
        if items and queryset:
            items = items.split(',')
            for item in items:
                if item.isdigit():
                    try:
                        OrderItem.objects.filter(order_id=queryset.id, id=item).delete()
                    except:
                        return JsonResponse({'Status': False, 'Error': 'Ошибка удаления из БД'})
                else:
                    JsonResponse({'Status': False, 'Error': 'Введите корректный номер заказа'}, status=403)
            return JsonResponse({'Status': 'Позиция(и) удалены'})
        else:
            return JsonResponse({'Status': False, 'Error': 'Не указаны все необходимые данные'}, status=403)


    """Изменить количество товара в позиции"""
    def put(self, request, *args, **kwargs):
        items = request.data.get('items')
        queryset_order = Order.objects.get(user_id=request.user.id, state='basket')
        if items and queryset_order:
            for item in items:
                if type(item['id']) == int and type(item['quantity']) == int:
                    try:
                        OrderItem.objects.filter(order_id=queryset_order.id, id=item['id']).update(
                            quantity=item['quantity'])

                    except:
                        return JsonResponse({'Status': False, 'Error': 'Ошибка записи в БД'})
                else:
                    return JsonResponse({'Status': False, 'Error': 'Не указаны все необходимые данные'}, status=403)
            return JsonResponse({'Status': 'Позиция(и) изменены'})
        else:
            return JsonResponse({'Status': False, 'Error': 'Не указаны все необходимые данные'}, status=403)



class OrderView(APIView):
    """Класс для работы с заказом"""
    permission_classes = [IsAuthorPermissions]

    """Подтвердить заказ из корзины"""
    def post(self, request, *args, **kwargs):
        if type(request.data.get('id')) == int and type(request.data.get('buyer')) == int:
            try:
                queryset = Order.objects.filter(user_id=request.user.id, id=request.data['id']).update(
                    buyer_id=request.data['buyer'],
                    state='new')
            except:
                return JsonResponse({'Status': False, 'Error': 'Ошибка записи в БД'})
            else:
                if queryset > 0:
                    return JsonResponse({'Status': 'Заказ оформлен'})
                else:
                    return JsonResponse({'Status': 'Не указаны все необходимые аргументы'})
        else:
            return JsonResponse({'Status': False, 'Error': 'Не указаны все необходимые аргументы'})

    """Показать оформленные заказы"""
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user_id=request.user.id).exclude(state='basket').distinct()
        if orders:
            list_orders = []
            for order in orders:
                order_items = OrderItem.objects.filter(order_id=order.id).distinct()
                if order_items:
                    total_price = 0
                    for item in order_items:
                        total_price += item.quantity * item.product_info.price
                    serializer = OrderItemSerializer(order_items, many=True)
                    list_orders.append({'items': serializer.data, 'total_price': total_price})
                else:
                    JsonResponse({'Status': False, 'Error': 'В одном из заказов удалены все позиции'}, status=403)
            return Response(list_orders)
        else:
            JsonResponse({'Status': False, 'Error': 'Нет оформленных заказов'}, status=403)


class ShopStatusView(APIView):
    """Класс для просмотра/изменения статуса магазина"""
    permission_classes = [IsShopPermissions]

    def get(self, request, *args, **kwargs):
        queryset = Shop.objects.filter(user_id=request.user.id).select_related('user').first()
        if queryset:
            serializer = ShopStatusSerializer(queryset)
            return Response(serializer.data)
        else:
            return JsonResponse({'Status': False, 'Errors': 'Нет привязанных к профилю магазинов'})

    def patch(self, request, *args, **kwargs):
        serializer = ShopStatusSerializer(data=request.data)
        if serializer.is_valid():
                try:
                    queryset = Shop.objects.filter(user_id=request.user.id).select_related('user').update(**serializer.validated_data)
                except ValueError as error:
                    return JsonResponse({'Status': False, 'Errors': str(error)})
                else:
                    if queryset > 0:
                        return Response(serializer.data)
                    else:
                        return JsonResponse({'Status': False, 'Errors': 'Нет привязанных к профилю магазинов'})
        else:
            return Response(serializer.errors)


class ShopOrdersView(APIView):
    """Класс для получения заказов поставщиками"""
    permission_classes = [IsShopPermissions]

    def get(self, request, *args, **kwargs):
        queryset = Order.objects.filter(order_items__product_info__shop__user_id=request.user.id).exclude(
            state='basket').prefetch_related('order_items__product_info__shop').distinct()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


class ShopUpdateView(APIView):
    """Класс для обновления прайса от поставщика"""
    permission_classes = [IsShopPermissions]

    def post(self, request, *args, **kwargs):
        # with open('C:\python\python-final-diplom\data\shop1.yaml', encoding="utf-8") as file:
        #     data = yaml.full_load(file)
        url = request.data.get('url')
        if url:
            stream = requests.get(url).content
            data = yaml.load(stream, Loader=yaml.FullLoader)

            shop = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id, url=url)[0]
            for category_data in data['categories']:
                category = Category.objects.get_or_create(name=category_data['name'])[0]
                category.shops.add(shop.id)
                category.save()
            ProductInfo.objects.filter(shop_id=shop.id).delete()

            for product_data in data['goods']:
                product = Product.objects.get_or_create(name=product_data['name'])[0]
                product_info = ProductInfo.objects.create(product_id=product.id, shop_id=shop.id,
                                                          price=product_data['price'], quantity=product_data['quantity'])

                for key, value in product_data['parameters'].items():
                    parameter = Parameter.objects.get_or_create(name=key)[0]
                    ProductParameter.objects.create(product_info_id=product_info.id,
                                                    parameter_id=parameter.id, value=value)

            return JsonResponse({'Status': 'Товары добавлены'})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые данные'})






