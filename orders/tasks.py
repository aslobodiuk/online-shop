# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import send_mail
from .models import Order

def OrderCreated(order_id):

    order = Order.objects.get(id=order_id)
    subject = 'Order number: {}'.format(order.id)
    message = 'Dear {}, your order is confirmed. Order number: {}'.format(order.first_name, order.id)
    mail_send = send_mail(subject, message, 'admin@myshop.ua', [order.email])
    return mail_send