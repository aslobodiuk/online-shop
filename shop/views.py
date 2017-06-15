# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

from cart.forms import CartAddProductForm
from cart.cart import Cart

from .models import Category, Product
from .filters import ProductFilter


def ProductList(request):
    products = Product.objects.all()
    f = ProductFilter(request.GET, queryset=products)
    return render(request, 'shop/product/list.html', {'filter': f})

def ProductDetail(request, id, slug):
    cart = Cart(request)
    cart_quantity = 0
    product = get_object_or_404(Product, id=id, slug=slug)
    for item in cart:
        if item["product"] == product:
            cart_quantity = cart[id]["quantity"]

    cart_product_form = CartAddProductForm(initial={'url': request.path})
    return render(request, 'shop/product/detail.html', {'product': product,
                            'cart_product_form': cart_product_form,
                            'cart_quantity': cart_quantity})