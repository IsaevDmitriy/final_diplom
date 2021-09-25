from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator



class ShopStatusChoices(models.TextChoices):
    """Статусы приёма заказов"""

    OPEN = "OPEN", "Открыт"
    CLOSED = "CLOSED", "Закрыт"


class Shop(models.Model):
    """Магазин (поставщик)"""

    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    state = models.CharField(verbose_name='Приём заказов', choices=ShopStatusChoices.choices, max_length=20,
                            default=ShopStatusChoices.OPEN)
    user = models.OneToOneField('User', verbose_name='Пользователь',
                                blank=True, null=True,
                                on_delete=models.CASCADE)

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
        verbose_name = 'Цена на товар в магазине'
        verbose_name_plural = "Список цен по магазинам"

    def __str__(self):
        return f'{self.shop} - {self.product}. Цена: {self.price}'



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

    BASKET = 'basket', 'Статус корзины'
    NEW = "new", "Новый"
    CONFIRMED = "confirmed", "Подтвержден"
    ASSEMBLED = "assembled", "Собран"
    SENT = "sent", "Отправлен"
    DELIVERED = "delivered", "Доставлен"
    CANCELED = "canceled", "Отменен"


class Order(models.Model):
    """Заказ"""
    user = models.ForeignKey('User', verbose_name='Пользователь',
                             related_name='orders', blank=True,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(verbose_name='Статус', choices=OrderStateChoices.choices, max_length=20,
                             default=OrderStateChoices.BASKET)
    buyer = models.ForeignKey('Buyer', verbose_name='Покупатель',
                                blank=True, null=True,
                                on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказов"

    def __str__(self):
        return f'{self.user} {str(self.created_at)} {self.state}'


class OrderItem(models.Model):
    """Позиции в заказе"""
    order = models.ForeignKey('Order', verbose_name='Заказ', related_name='order_items', blank=True,
                              on_delete=models.CASCADE)
    product_info = models.ForeignKey('ProductInfo', verbose_name='Информация о продукте', related_name='order_items',
                                     blank=True,
                                     on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = "Список элементов заказа"

    def __str__(self):
        return f'Заказ:{self.order} | Продукт:{self.product_info} | Количество:{self.quantity}'


class UserTypeChoices(models.TextChoices):
    """Типы пользователей"""

    SHOP = "shop", "Магазин"
    BUYER = "buyer", "Покупатель"



class User(AbstractUser):
    """Пользователь"""


    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    type = models.CharField(verbose_name='Тип пользователя', choices=UserTypeChoices.choices,
                            default=UserTypeChoices.BUYER, max_length=20)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    company = models.CharField(verbose_name='Компания', max_length=40, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


    def __str__(self):
        return f'{self.username} {self.type} {self.company} {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"




class Buyer(models.Model):
    """Контакты покупателя при доставке"""
    user = models.ForeignKey('User', verbose_name='Пользователь',
                             related_name='contacts', blank=True,
                             on_delete=models.CASCADE)
    address = models.CharField(max_length=300, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    name = models.CharField(verbose_name='Имя', max_length=100)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = "Список покупателей"

    def __str__(self):
        return f'{self.name} - {self.address}'











