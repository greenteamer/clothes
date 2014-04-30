# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url, include
from webshop import settings


urlpatterns = patterns('webshop.checkout.views',

    url(r'^result/$', 'payment_received', name='payment_received'),

    url(r'^success/$', {'template_name': 'robokassa/success.html'}, name='robokassa_success'),
    url(r'^fail/$', {'template_name': 'robokassa/fail.html'}, name='robokassa_fail'),
    url(r'^error/$', {'template_name': 'robokassa/error.html'}, name='robokassa_error'),
)
