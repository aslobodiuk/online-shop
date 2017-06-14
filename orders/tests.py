# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
from django.core import mail

from .tasks import OrderCreated
from .models import Order, OrderItem

class OrderItemTestCase(TestCase):

    fixtures = ['shop', 'orders']

    def test_get_cost(self):
        order_item = OrderItem.objects.first()
        self.assertEqual(order_item.get_cost(), order_item.price * order_item.quantity)

class OrderTestCase(TestCase):
    
    fixtures = ['shop', 'orders']

    def test_get_total_cost(self):
        order = Order.objects.first()
        self.assertEqual(order.get_total_cost(), sum(item.get_cost() for item in order.items.all()))

class ViewsTestCase(TestCase):

    fixtures = ['shop', 'orders']

    def test_order_create(self):
        response = self.client.get(reverse('orders:OrderCreate'))
        self.assertEqual(response.status_code, 200)

        post_response = self.client.post(reverse('orders:OrderCreate'))
        self.assertEqual(post_response.status_code, 200)

    def test_admin_order_detail(self):
        order = Order.objects.first()
        response = self.client.get(reverse('orders:AdminOrderDetail', args=[order.id]))
        self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.context["order"], order)

    def test_admin_order_pdf(self):
        order = Order.objects.first()
        response = self.client.get(reverse('orders:AdminOrderPDF', args=[order.id]))
        self.assertEqual(response.status_code, 302)

class OrderCreatedMailTestCase(TestCase):

    fixtures = ['shop', 'orders']

    def test_send_confirmation_mail(self):
        order = Order.objects.first()
        
        #Send mail
        OrderCreated(order.id)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Order number: {}'.format(order.id))
        self.assertEqual(mail.outbox[0].from_email, 'admin@myshop.ua')
        self.assertEqual(mail.outbox[0].to, [order.email])
        self.assertEqual(mail.outbox[0].body,
            'Dear {}, your order is confirmed. Order number: {}'.format(order.first_name, order.id))