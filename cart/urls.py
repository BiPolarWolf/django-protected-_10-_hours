from django.urls import path
from cart import views



app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart-view'),
    path('add/', views.cart_add_view, name='add-to-cart'),
    path('delete/',views.cart_delete_view,name ='delete-from-cart'),
    path('update/',views.cart_update_view,name='cart-update')
]
