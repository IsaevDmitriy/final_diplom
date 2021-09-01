from django.db import models


class ShopStatusChoices(models.TextChoices):
    """Статусы приёма заказов"""

    OPEN = "OPEN", "Открыт"
    CLOSED = "CLOSED", "Закрыт"


class Shop(models.Model):
    """Магазин (поставщик)"""

    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)    # Адрес с которого будут приходить yaml с информацией о заказах
    state = models.CharField(verbose_name='Приём заказов', choices=ShopStatusChoices.choices,
                            default=ShopStatusChoices.OPEN)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категории товаров"""

    name = models.CharField(max_length=50, verbose_name='Название')
    shops = models.ManyToManyField('Shop', verbose_name='Магазины', related_name='categories', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар"""

    name = models.CharField(max_length=50, verbose_name='Название')
    category = models.ForeignKey('Category', verbose_name='Категория', related_name='products', blank=True, null=True,
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = "Список продуктов"

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    """Информация о товарах в конкретном магазине"""

    product = models.ForeignKey('Product', verbose_name='Продукт', related_name='product_infos', blank=True,
                                on_delete=models.CASCADE)
    shop = models.ForeignKey('Shop', verbose_name='Магазин', related_name='product_infos', blank=True,
                                     on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')


    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = "Информационный список о продуктах"



class Parameter(models.Model):
    """Уникальные параметры товара"""
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Имя параметра'
        verbose_name_plural = "Имена параметров"

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    """Информация о параметрах товара в магазине"""
    product_info = models.ForeignKey('ProductInfo', verbose_name='Информация о продукте',
                                     related_name='product_parameters', blank=True,
                                     on_delete=models.CASCADE)
    parameter = models.ForeignKey('Parameter', verbose_name='Параметр', related_name='product_parameters', blank=True,
                                  on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = "Список параметров"

    def __str__(self):
        return f'{self.parameter} {self.product_info} {self.value}'


class OrderStateChoices(models.TextChoices):
    """Статусы доставки товара."""

    NEW = "new", "Новый"
    CONFIRMED = "confirmed", "Подтвержден"
    ASSEMBLED = "assembled", "Собран"
    SENT = "sent", "Отправлен"
    DELIVERED = "delivered", "Доставлен"
    CANCELED = "canceled", "Отменен"


class Order(models.Model):
    """Дата создания, автор и статус заказа"""
    user = models.ForeignKey('User', verbose_name='Пользователь',
                             related_name='orders', blank=True,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(verbose_name='Статус', choices=OrderStateChoices.choices, default=OrderStateChoices.NEW)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказов"

    def __str__(self):
        return f'{self.user} {str(self.created_at)} {self.state}'


class OrderItem(models.Model):
    """Магазины и цены в заказе"""
    order = models.ForeignKey('Order', verbose_name='Заказ', related_name='order_items', blank=True,
                              on_delete=models.CASCADE)
    product_info = models.ForeignKey('ProductInfo', verbose_name='Информация о продукте', related_name='order_items',
                                     blank=True,
                                     on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Подробный заказ'
        verbose_name_plural = "Список подробных заказов"

    def __str__(self):
        return f'{self.product_info} {self.quantity}'


class UserTypeChoices(models.TextChoices):
    """Типы покупателей"""

    SHOP = "shop", "Магазин"
    BUYER = "buyer", "Покупатель"


class User(models.Model):
    """Покупатель"""
    name = models.CharField(verbose_name='Имя', max_length=100)
    type = models.CharField(verbose_name='Тип пользователя', choices=UserTypeChoices.choices,
                            default=UserTypeChoices.SHOP)

    class Meta:
        verbose_name = 'Имя параметра'
        verbose_name_plural = "Имена параметров"

    def __str__(self):
        return f'{self.type} {self.name}'