# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from cart.forms import CartAddProductForm

from .models import Product

class ProductTestCase(TestCase):
    
    fixtures = ['shop']

    def test_get_absolute_url(self):
        prod = Product.objects.first()
        self.assertEqual(prod.get_absolute_url(), '/' + str(prod.id) + '/' + prod.slug + '/')

class ViewsTestCase(TestCase):

    fixtures = ['shop']

    def test_detail(self):
        prod = Product.objects.first()
        cart_product_form = CartAddProductForm(initial={'url': '/'})
        response = self.client.get(prod.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"], prod)
        #self.assertEqual(response.context["cart_product_form"], cart_product_form)
        

    def test_all_list(self):
        response = self.client.get(reverse('shop:ProductList'))
        self.assertEqual(response.status_code, 200)