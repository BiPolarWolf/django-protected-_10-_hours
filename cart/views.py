from calendar import c
from decimal import Decimal
from django.shortcuts import render,get_object_or_404
from .cart import Cart
from shop.models import ProductProxy
from django.http import JsonResponse

def cart_view(request):
    return render(request, 'cart/cart_view.html')

def cart_add_view(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(ProductProxy, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_qty = cart.__len__()

        response = JsonResponse({'qty': cart_qty,'product':product.title})
        return response

def cart_delete_view(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.remove(product_id)
        response = JsonResponse({'qty': cart.__len__()})
        return response

def cart_update_view(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product_id,product_qty)
        total = cart.get_total_price()
        response = JsonResponse({'qty':cart.__len__(),'total':total})
        return response
