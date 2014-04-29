# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.db import models
from webshop.catalog.models import Product

# Create your models here.
class Slider(models.Model):
    image = models.ImageField(upload_to='slider', verbose_name=u'фото для слайдера')
    product = models.ForeignKey(Product, verbose_name=u'Выбрать продукт')

    def __unicode__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = (u'Слайды')
        verbose_name = (u'Слайдер на главной странице')
