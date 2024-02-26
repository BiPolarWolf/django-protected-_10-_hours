from re import S
from urllib import response
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


from .models import ProductProxy, Category, Product



class ProductsViewTests(TestCase):


    def test_products_view(self):

        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )
        category = Category.objects.create(name='Django')
        uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        product_1 = Product.objects.create(title='Product 1', category=category, image=uploaded,slug='product-1')
        product_2 = Product.objects.create(title='Product 2', category=category, image=uploaded,slug='product-2')
        
        
        response = self.client.get(reverse('shop:products'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 2)
        self.assertEqual(response.context['products'][0], product_1)
        
        self.assertContains(response, product_1)
        self.assertContains(response, 'Product 2')


class ProductDetailViewTest(TestCase):
    def test_get_product_by_slug(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        
        # create uploaded file
        uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        
        # Create Category and Product
        category = Category.objects.create(name='Django')
        product = Product.objects.create(title='Product 1', category=category, image=uploaded,slug='product-1')


        response = self.client.get(reverse('shop:product_detail', kwargs={'slug': 'product-1'}))


        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)
        self.assertEqual(response.context['product'].slug, 'product-1')


class CategoryViewTest(TestCase):

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        # create uploaded file
        uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        
        # Create Category and Product
        self.category = Category.objects.create(name='Django')
        self.product = Product.objects.create(title='Product 1', category=self.category, image=uploaded,slug='product-1')


    def test_status_code(self):
        response = self.client.get(reverse('shop:products_by_category', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)



    def test_tamplate_used(self):
        response = self.client.get(reverse('shop:products_by_category', kwargs={'slug': self.category.slug}))
        self.assertTemplateUsed(response, 'shop/products_by_category.html')
    
    

    def test_context_data(self):
        response = self.client.get(reverse('shop:products_by_category', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'][0], self.product)
        


    