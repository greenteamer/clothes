#-*-coding:utf-8-*-
from dajax.core import Dajax
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from dajaxice.decorators import dajaxice_register
from django.core.mail import send_mail
from dajaxice.utils import deserialize_form
from webshop.settings import ADMIN_EMAIL

from webshop.catalog.forms import ProductOneClickForm
from webshop.checkout.forms import MainForm
from webshop.checkout.models import OrderOneClick


@dajaxice_register
def send_form(request, form):
    dajax = Dajax()
    form = ProductOneClickForm(deserialize_form(form))
    dajax.remove_css_class('#loader2', 'hidden')
    if form.is_valid():
        dajax.remove_css_class('#my_form input', 'error')
        dajax.remove_css_class('#loader2', 'hidden')

        # result = u'Отправляем сообщение'
        # dajax.assign('#status', 'value', result)

        phone = form.cleaned_data.get('phone')
        product_name = form.cleaned_data.get('product_name')
        date = datetime.now()
        dateFormat = DateFormat(date)
        dateFormat = dateFormat.format(get_format('DATE_FORMAT'))
        subject = u'Заявка в 1 клик %s' % dateFormat
        message = u'Дата: %s \n Телефон: %s \n Товар: %s' % (dateFormat, phone , product_name)
        send_mail(subject, message, 'teamer777@gmail.com', [ADMIN_EMAIL], fail_silently=False)

        order = OrderOneClick(phone=phone , product_name=product_name)
        order.save()

        # dajax.remove_css_class('#status', 'hidden')
        # result = u'Сообщение отправлено'
        # dajax.assign('#status', 'value', result)
        dajax.remove_css_class('#message_show', 'hidden')
        # dajax.script('closemodal()')



        # dajax.redirect('/', delay=2000)
        # dajax.code('$(".close").click()')

    else:
        dajax.remove_css_class('#my_form input', 'error')
    #     dajax.remove_css_class('#status', 'hidden')
    #     result = u'Введите данные'
    #     dajax.assign('#status', 'value', result)
        for error in form.errors:
            dajax.add_css_class('#id_%s' % error, 'error')

    dajax.add_css_class('#loader2', 'hidden')
    return dajax.json()


@dajaxice_register
def mainForm(request, form):
    dajax = Dajax()
    form = MainForm(deserialize_form(form))
    dajax.remove_css_class('#loader', 'hidden')
    if form.is_valid():
        dajax.remove_css_class('#loader', 'hidden')
        dajax.remove_css_class('#mainForm input', 'error')
        phone = form.cleaned_data.get('phone')
        subject = u'podarkoff-moscow.ru Заявка'
        message = u'Телефон: %s' % (phone)
        send_mail(subject, message, 'teamer777@gmail.com', [ADMIN_EMAIL], fail_silently=False)

        dajax.remove_css_class('#message_show', 'hidden')
        dajax.script('closemodal()')

    else:
        dajax.remove_css_class('#mainForm input', 'error')
        for error in form.errors:
            dajax.add_css_class('#id_%s' % error, 'error')

    dajax.add_css_class('#loader', 'hidden')
    return dajax.json()
