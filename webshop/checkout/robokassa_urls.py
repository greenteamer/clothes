# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, url, include
from webshop import settings
from webshop.checkout.views import robokassa_result, RobokassaSuccess, RobokassaFail


urlpatterns = patterns('webshop.checkout.views',
    url(r'^result$', robokassa_result, name='robokassa_result'),
    url(r'^success$', RobokassaSuccess.as_view(), name='robokassa_success'),
    url(r'^fail$', RobokassaFail.as_view(), name='robokassa_fail'),
)
