from django_filters import rest_framework as filters
from backend.models import ProductInfo


class ProductInfoFilter(filters.FilterSet):
    """Фильтры для товаров."""

    price_from = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_to = filters.NumberFilter(field_name='price', lookup_expr='lte')
    shop = filters.MultipleChoiceFilter(field_name='shop', queryset=ProductInfo.objects.all())
    product = filters.MultipleChoiceFilter(field_name='product', queryset=ProductInfo.objects.all())
    category = filters.MultipleChoiceFilter(field_name='product__category', queryset=ProductInfo.objects.all())

    class Meta:
        model = ProductInfo
        fields = ['shop', 'product', 'price_from', 'price_to', 'category']

