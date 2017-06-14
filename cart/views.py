# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse

from shop.models import Product

from .cart import Cart
from .forms import CartAddProductForm



@require_POST
def CartAdd(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    is_error = False
    if form.is_valid():
        cd = form.cleaned_data
        is_error = cart.add(product=product, quantity=cd['quantity'],
                                  update_quantity=cd['update'])
    if is_error: return HttpResponseRedirect(reverse('cart:Sorry') + "?next=" + request.POST['url'])
    else: return redirect('cart:CartDetail')

def CartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:CartDetail')

def CartDetail(request):
    cart = Cart(request)
    for item in cart: 
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True,
                                            'url': request.path
                                        })
    return render(request, 'cart/detail.html', {'cart': cart})

def Sorry(request):
    url = request.GET['next']
    return render(request, "cart/sorry.html", {'next': url})