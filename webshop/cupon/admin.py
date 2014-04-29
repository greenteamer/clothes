# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from webshop.cupon.models import Cupon

admin.site.register(Cupon)