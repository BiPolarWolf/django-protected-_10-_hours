from decimal import Decimal
from shop.models import ProductProxy



class Cart():
    def __init__(self,request) -> None:
        self.session = request.session
        cart = self.session.get('session_key')
        
        if cart is None :
            cart= self.session['session_key'] = {}

        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = ProductProxy.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item

    def add(self,product,quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'qty': 0, 'price': str(product.price)}

        self.cart[product_id]['qty'] += quantity
        self.session.modified = True


    def remove(self,product_pk):
        product_id = str(product_pk)
        if product_id in self.cart.keys():
            del self.cart[product_id]
        self.session.modified = True


    def update(self,product_id, product_qty):
        self.cart[str(product_id)]['qty'] = product_qty
        self.session.modified = True


    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())
         
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
        