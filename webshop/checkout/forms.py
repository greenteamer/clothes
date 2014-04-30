# -*- coding: utf-8 -*-
#!/usr/bin/env python
import datetime
import re

from django import forms
from django.forms import ModelForm, Textarea, TextInput
from django.utils.translation import ugettext_lazy as _
from django.core.validators import email_re
from django.utils.encoding import smart_unicode

from webshop import settings
from models import Order


class ContactForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ('status', 'ip_address', 'user', 'transaction_id',)
        # widgets = {
        #     'cupon': TextInput(),
        # }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        # переопределяем аттрибуты по умолчанию
        for field in self.fields:
            self.fields[field].widget.attrs['size'] = '30'

    def clean_phone(self):
        """Проверка телефонного номера (>10 цифр)"""
        phone = self.cleaned_data['phone']
        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 11:
            raise forms.ValidationError(_(u"""
            Введите правильный телефон, например (8-920-351-21-21 или 89203512121)"""))
        return self.cleaned_data['phone']

def strip_non_numbers(data):
    """Удаляет все символы которые не являются числом
    >>> strip_non_numbers('988f2ds2')
    '98822'
    """
    non_numbers = re.compile('\D')
    return non_numbers.sub('', data)

"""форма заказа на всех страницах"""
class MainForm(forms.Form):
    name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=20)
    text = forms.Textarea()

    def clean_phone(self):
        """Проверка телефонного номера (>10 цифр)"""
        phone = self.cleaned_data['phone']
        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 11:
            raise forms.ValidationError(_(u"""
            Введите правильный телефон, например (8-920-351-21-21 или 89203512121)"""))
        return self.cleaned_data['phone']



# class CheckoutForm(forms.Form):
#     email = forms.EmailField(max_length=50)
#     phone = forms.CharField(max_length=20)
#     shipping_name = forms.CharField(max_length=50)
#     shipping_address_1 = forms.CharField(max_length=50)
#     shipping_city = forms.CharField(max_length=50)
#     cupon = forms.CharField(max_length=50)
    # class Meta:
        # model = Order
        # exclude = ('status', 'ip_address', 'user', 'transaction_id', 'cupon', )
        # fields = ('email', 'phone', 'shipping_name', 'shipping_address_1', 'shipping_city',)

