# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse

from shop.models import Product

from .cart import Cart

class ViewsTestCase(TestCase):

    fixtures = ['shop']

    def test_cart_add(self):
        product = Product.objects.first()
        response = self.client.post(reverse('cart:CartAdd', args=[product.id]))
        self.assertEqual(response.status_code, 302)

    def test_cart_remove(self):
        product = Product.objects.first()
        response = self.client.get(reverse('cart:CartRemove', args=[product.id]))
        self.assertEqual(response.status_code, 302)

    def test_cart_detail(self):
        response = self.client.get(reverse('cart:CartDetail'))
        self.assertEqual(response.status_code, 200)

    def test_sorry_page(self):
        product = Product.objects.first()
        response = self.client.get(reverse('cart:Sorry') + "?next=" + product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['next'], product.get_absolute_url())

class CartTestCase(TestCase):

    fixtures = ['shop']

    def setUp(self):
        factory = RequestFactory()
        request = factory.get(reverse('shop:ProductList'))
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        
        self.cart = Cart(request)

    def test_add_method_with_two_different_products(self):
        
        product1 = Product.objects.first()
        product1_cnt = 2
        product2 = Product.objects.last()
        product2_cnt = 3

        self.cart.add(product1, product1_cnt)
        self.cart.add(product2, product2_cnt)

        self.assertEqual(self.cart.get_total_price(), product1.price*product1_cnt + product2.price*product2_cnt)
        self.assertEqual(len(self.cart), product1_cnt + product2_cnt)

        for item in self.cart:
            if item['product'] == product1:
                product = product1
                cnt = product1_cnt
            else:
                product = product2
                cnt = product2_cnt

            self.assertEqual(item['price'], product.price)
            self.assertEqual(item['total_price'], product.price*cnt)
            self.assertEqual(item['quantity'], cnt)

    def test_add_method_with_one_product(self):

        product = Product.objects.first()
        cnt1 = 1
        cnt2 = 2

        """test with update_quantity = False"""
        self.cart.add(product, cnt1, False)
        self.cart.add(product, cnt2, False)
        self.assertEqual(len(self.cart), cnt1 + cnt2)

        """test with update_quantity = True"""
        self.cart.add(product, cnt1, True)
        self.assertEqual(len(self.cart), cnt1)

    def test_remove_method(self):

        product = Product.objects.first()
        cnt = 3

        self.cart.add(product, cnt)
        self.assertEqual(len(self.cart), cnt)
        self.cart.remove(product)
        self.assertEqual(len(self.cart), 0)
