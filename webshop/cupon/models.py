# -*- coding: utf-8 -*-
from django.db import models

class Cupon(models.Model):
    name = models.CharField(verbose_name=u'Название купона', max_length=256)
    identifier = models.CharField(verbose_name=u'Идентификатор', max_length=256)
    percent = models.CharField(verbose_name=u'Процент скидки', max_length=10)

    def __unicode__(self):
        return self.name


