from urllib import response
from django.test import TestCase, Client, RequestFactory

import json

from django.contrib.sessions.middleware import SessionMiddleware

from shop.models import ProductProxy, Category
from django.urls import reverse

from .views import cart_view, cart_add_view, cart_delete_view, cart_update_view



class CartViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory().get(reverse('cart:cart-view'))
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()


    def test_cart_view(self):
        request = self.factory
        response = cart_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.client.get(reverse('cart:cart-view')), 'cart/cart_view.html')

class CartAddViewTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product',category=self.category,price=10.0)
        self.factory = RequestFactory().post(reverse('cart:add-to-cart'),{'action':'post','product_id':self.product.id,'product_qty':2})

        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_add(self):
        request = self.factory
        response = cart_add_view(request)
        self.assertEqual(response.status_code,200)
        data = json.loads(response.content)
        self.assertEqual(data['product'],'Example Product')
        self.assertEqual(data['qty'],2)

class CartDeleteViewTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product',category=self.category,price=10.0)
        self.factory = RequestFactory().post(reverse('cart:delete-from-cart'),{'action':'post','product_id':self.product.id})

        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_delete(self):
        request = self.factory
        response = cart_delete_view(request)
        self.assertEqual(response.status_code,200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'],0)



class CartUpdateViewTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product',category=self.category,price=10.0)
        self.factory = RequestFactory().post(reverse('cart:add-to-cart'),{'action':'post','product_id':self.product.id,'product_qty':1})
        self.factory= RequestFactory().post(reverse('cart:cart-update'),{'action':'post','product_id':self.product.id,'product_qty':2})
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()



    def test_cart_update(self):
        request = self.factory
        response = cart_add_view(request)
        response = cart_update_view(request)
        
        self.assertEqual(response.status_code,200)

        data = json.loads(response.content)

        self.assertEqual(data['qty'],2)
        self.assertEqual(data['total'],'20.00')