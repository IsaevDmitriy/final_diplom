"""orders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from backend.views import ProductView, ShopView, ShopStatusView, ProductInfoView, BasketView, BuyerView, \
    ShopUpdateView, CategoryView, OrderView, ShopOrdersView, RegisterAccountView, AccountDetailsView, TokenAccountView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/partner/state/', ShopStatusView.as_view(), name='shop_status'),
    path('api/v1/partner/update/', ShopUpdateView.as_view(), name='shop_update'),
    path('api/v1/partner/orders/', ShopOrdersView.as_view(), name='shop_orders'),

    path('api/v1/categories/', CategoryView.as_view(), name='categories'),
    path('api/v1/shops/', ShopView.as_view(), name='shop'),
    path('api/v1/products/', ProductInfoView.as_view(), name='products_filter'),
    path('api/v1/product/', ProductView.as_view(), name='product'),
    path('api/v1/basket/', BasketView.as_view(), name='basket'),
    path('api/v1/order/', OrderView.as_view(), name='order'),

    path('api/v1/user/contact/', BuyerView.as_view(), name='user-contact'),
    path('api/v1/user/register/', RegisterAccountView.as_view(), name='register'),
    path('api/v1/user/login/', TokenAccountView.as_view(), name='login'),
    path('api/v1/user/details/', AccountDetailsView.as_view(), name='details')
]
