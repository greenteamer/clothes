# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView

from webshop.checkout.models import Order, OrderItem
from webshop.checkout import checkout
from webshop.cart import cart

from django.core.mail import send_mail, EmailMultiAlternatives
from webshop.checkout.forms import ContactForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from robokassa.signals import result_received
from django.template.loader import render_to_string
from webshop.settings import ADMIN_EMAIL

from robokassa.forms import RobokassaForm


"""обработа контактных данных и создание сущности Order"""
def contact(request, template_name='checkout/checkout.html'):
    if cart.is_empty(request):
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        phone = request.POST['phone']

        if form.is_valid():

            form.clean_phone()
            response = checkout.process(request)

            order = response.get('order', 0)
            order_id = order.id

            if order_id:
                request.session['order_id'] = order_id
                receipt_url = urlresolvers.reverse('checkout_receipt')

                return HttpResponseRedirect(receipt_url)
        else:
            form = ContactForm(request.POST)
            return render(request, 'checkout/checkout.html', {
                'form': form,
                'error': form.errors,
            })
    else:
        form = ContactForm()
        # post = Post.objects.all()

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# @login_required
"""подготавливаем данные к оплате"""
def receipt_view(request, template_name='checkout/receipt.html'):
    """Представление отображающее сделанный заказ"""
    order_id = request.session.get('order_id', '')
    if order_id:
        # если в cookies есть номер заказа, выводим его содержимое
        order = Order.objects.filter(id=order_id)[0]
        order_items = OrderItem.objects.filter(order=order)

        if order.payment_method == 2:
            form = RobokassaForm(initial={
                   'OutSum': order.total,
                   'InvId': order.id,
                   'Desc': order.shipping_name,
                   'Email': order.email,
                   # 'IncCurrLabel': '',
                   # 'Culture': 'ru'
               })
        else:

            """отправка писем"""
            items = ''
            for item in order_items:
                items = items + '%s \n' % item.name
            if order.payment_method == 1:
                payment_method = u'Оплата курьером'
            else:
                payment_method = u'Оплата онлайн'
            subject = u'podarkoff-moscow.ru заявка от %s' % order.shipping_name
            message = u'Заказ №: %s \n Имя: %s \n телефон: %s \n почта: %s \n id заказа: %s \n Товары: %s \n К оплате курьером: %s \n Способ оплаты: %s' % (order.transaction_id, order.shipping_name, order.phone, order.email, order.id, items, order.total, payment_method)
            send_mail(subject, message, 'teamer777@gmail.com', [ADMIN_EMAIL], fail_silently=False)

            context_dict = {
                    'transaction': order.transaction_id,
                    'id': order.id,
                    'items': items,
                    'total': order.total,
                    'payment_method': payment_method,
                }

            message = render_to_string('checkout/email.html', context_dict)
            from_email = 'teamer777@gmail.com'
            to = '%s' % order.email
            msg = EmailMultiAlternatives(subject, message, from_email, [to])
            msg.content_subtype = "html"
            msg.send()


        del request.session['order_id']
    else:
        # иначе перенаправляем пользователя на страницу корзины
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# """обозначаем шаблоны robokassa"""
# class RobokassaSuccess(TemplateView):
#     template_name = 'robokassa/success.html'
#
#
# class RobokassaFail(TemplateView):
#     template_name = 'robokassa/fail.html'
#
#
# class RobokassaError(TemplateView):
#     template_name = 'robokassa/error.html'
#
#
# def robokassa_result(request):
#     return render(request, 'robokassa/result.html')


"""обрабатываем сигналы"""
def payment_received(sender, **kwargs):
    order = Order.objects.get(id=kwargs['InvId'])
    order.status = Order.PAID
    # order.paid_sum = kwargs['OutSum']
    order.save()

    """отправка писем"""
    # order_items = OrderItem.objects.filter(order=order)
    # items = ''
    # for item in order_items:
    #     items = items + '%s \n' % item.name
    # if order.payment_method == 1:
    #     payment_method = u'Оплата курьером'
    # else:
    #     payment_method = u'Оплата онлайн'
    # subject = u'podarkoff-moscow.ru заявка от %s' % order.shipping_name
    # message = u'Заказ №: %s \n Имя: %s \n телефон: %s \n почта: %s \n id заказа: %s \n Товары: %s \n Стоимость: %s \n Способ оплаты: %s' % (order.transaction_id, order.shipping_name, order.phone, order.email, order.id, items, order.total, payment_method)
    # send_mail(subject, message, 'teamer777@gmail.com', [ADMIN_EMAIL], fail_silently=False)
    #
    # context_dict = {
    #         'transaction': order.transaction_id,
    #         'id': order.id,
    #         'items': items,
    #         'total': order.total,
    #         'payment_method': payment_method,
    #     }
    #
    # message = render_to_string('checkout/email.html', context_dict)
    # from_email = 'teamer777@gmail.com'
    # to = '%s' % order.email
    # msg = EmailMultiAlternatives(subject, message, from_email, [to])
    # msg.content_subtype = "html"
    # msg.send()

result_received.connect(payment_received)