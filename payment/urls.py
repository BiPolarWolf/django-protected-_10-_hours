from .views import *

from django.urls import path

app_name = 'payment'

urlpatterns = [
    path('shipping/',shipping,name='shipping'),
    path('checkout/',checkout,name='checkout'),
    path('payment-success/',payment_success,name='payment-success'),
    path('payment-fail/',payment_fail,name='payment-failed'),
    path('complete-order/',complete_order,name='complete-order'),

]