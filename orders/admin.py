# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from .models import Order, OrderItem


def ExportToCSV(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; \
        filename=Orders-{}.csv'.format(datetime.datetime.now().strftime("%d/%m/%Y"))
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    writer.writerow([field.verbose_name.encode('utf-8') for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            elif not isinstance(value, (int, long, float, complex)):
            	value = getattr(obj, field.name).encode('utf-8')

            data_row.append(value)
        writer.writerow(data_row)
    return response
    ExportToCSV.short_description = 'Export CSV'

def OrderDetail(obj):
    return format_html('<a href="{}">Посмотреть</a>'.format(
        reverse('orders:AdminOrderDetail', args=[obj.id])
    ))

def OrderPDF(obj):
    return format_html('<a href="{}">PDF</a>'.format(
        reverse('orders:AdminOrderPDF', args=[obj.id])
    ))
OrderPDF.short_description = 'В PDF'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_field = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'city', 'paid', 'created', 'updated', OrderDetail, OrderPDF]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [ExportToCSV]

admin.site.register(Order, OrderAdmin)
