# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url, include
from webshop import settings


urlpatterns = patterns('webshop.checkout.views',
    url(r'^result/$', 'payment_received', name='payment_received'),
)
