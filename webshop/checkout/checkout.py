# -*- coding: utf-8 -*-
#!/usr/bin/env python
#import urllib
import random

from django.utils.translation import ugettext_lazy as _
from django.core import urlresolvers

#from webshop.checkout import google_checkout
from webshop.cart import cart
from webshop.checkout.models import Order, OrderItem
from webshop.checkout.forms import CheckoutForm, ContactForm
from webshop.accounts import profile
#from webshop.checkout import authnet
#from webshop import settings


class TransactionResultType:
    """Возможные результаты транзакции"""
    APPROVED = '1'
    DECLINED = '2'
    ERROR = '3'
    HELD_FOR_REVIEW = '4'


def get_checkout_url(request):
    """Возвращает the URL для модуля оплаты"""
    # для Google Checkout API:
    # return google_checkout.get_checkout_url(request)
    return urlresolvers.reverse('checkout')

def process(request):

    transaction_id = random.randint(1, 999999)
    order = create_order(request, transaction_id)
    results = {'order_number': order.id, 'order': order}

    return results


def create_order(request, transaction_id):
    """
    Если POST запрос к платежной системе успешен, создаем новый заказ содержащий товары из корзины
    Сохраняем заказ с идентификатором транзации который вернет шлюз платежной системы
    В конце делаем очистку корзины
    """
    order = Order()
    checkout_form = ContactForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)



    order.transaction_id = transaction_id
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.user = None
    if request.user.is_authenticated():
        order.user = request.user
    order.status = Order.SUBMITTED
    order.save()

    if order.pk:
        # Если заказ сохранен
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            # Создаем товар в заказе для каждого товара в корзине
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price
            oi.product = ci.product
            oi.save()
        # Очищаем корзину после оформления заказа
        cart.empty_cart(request)
        # Сохраняем введенные данные для будующих заказов
        if request.user.is_authenticated():
            profile.set(request)

        # Сохраняем информацию о профиле пользователя
        if request.user.is_authenticated():
            profile.set(request)
    # Возвращаем объект - новый заказа
    return order
