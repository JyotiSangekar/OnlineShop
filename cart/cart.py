from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon
import taxjar
from taxjar.response import TaxJarResponse
from jsonobject import *
import json
import requests

    
class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_client_ip(request, self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
                                                                                                                                                     
    def get_total_tax(self):
        ipad = requests.get("http://httpbin.org/ip", stream=True)
        ipadd = ipad.json()
        ipaddress = ipadd['origin']
        # ipaddress = get_client_ip(request, self)
        print(ipaddress)
        gurl = requests.get("http://api.ipinfodb.com/v3/ip-city/?key=c5da50983b3e0fecf2b442da5d9edfc127ef1e86b9031086ef84e041639ccbc4&ip=" + ipaddress + "&format=json")
        # print(gurl)
        g = gurl.json()
        zipc = g['zipCode']
        print(zipc)
        try:
            client = taxjar.Client(api_key='cc16b8b2f3fba39495891baf6a85e51c')
            rates = client.rates_for_location(str(zipc))
            print("there is zipc")
            print(rates)
            taxamount = rates['combined_rate']
            return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()) * Decimal(taxamount)
        except Exception as e:
            zipc = '90404'
            client = taxjar.Client(api_key='cc16b8b2f3fba39495891baf6a85e51c')
            rates = client.rates_for_location(zipc)
            print("there is no zipc")
            print(rates)
            taxamount = rates['combined_rate']
            return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()) * Decimal(taxamount)            
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()) * Decimal(taxamount)

    # def rates_for_location(self, postal_code, location_deets=None):
    #     """Shows the sales tax rates for a given location."""
    #     request = self._get("rates/" + postal_code, location_deets)
    #     return self.responder(request)

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return (self.get_total_price() - self.get_discount()) + self.get_total_tax()