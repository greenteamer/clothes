# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import template
from django.contrib.flatpages.models import FlatPage
from django.template import context

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from webshop.cart import cart
from webshop.catalog.models import Category, Product, ProductImage
from webshop.checkout import checkout
from webshop.catalog.models import Category


register = template.Library()

# @register.inclusion_tag("tags/cart_box.html")
# def cart_box(request):
# 	"""Вставка для виджета отображающего количество разных товаров в корзине"""
# 	cart_items = cart.get_cart_items(request)
#
#     # cart_item_count = cart.cart_distinct_item_count(request)
#     # cart_items = cart.get_cart_items(request)
# 	return {'cart_items': cart_items }

@register.inclusion_tag("tags/category_list.html")
def categories_tree(request):
	"""Возвращает дерево категорий"""
	return {'nodes': Category.objects.filter(is_active=True) }

@register.inclusion_tag("tags/footer.html")
def footer_links():
	"Вставка для виджета отображающего ссылки на статические страницы внизу"
    # products = Product.objects.all()
	flatpage_list = FlatPage.objects.all()
	return {'flatpage_list': flatpage_list }

# The first argument *must* be called "context" here.
def cart_box(context, request):
    cart_i = cart.get_cart_items(request)
    return {
        # 'products': products,
        'cart_i': cart_i,
    }
# Register the custom tag as an inclusion tag with takes_context=True.
register.inclusion_tag('tags/cart_box.html', takes_context=True)(cart_box)
