from django.urls import path
from .views import products_view, product_detail_view, products_by_category_view


app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('<slug:slug>/', product_detail_view, name='product_detail'),
    path('search/<slug:slug>/', products_by_category_view, name='products_by_category'),
]
