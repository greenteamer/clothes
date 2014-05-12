# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from webshop.cart import cart
from webshop.catalog.forms import *
from django.core.mail import send_mail
from webshop.catalog.models import Category, Product, Characteristic, ProductImage
from webshop.news.models import News


def index_view(request, template_name="catalog/index.html"):
    """Представление главной страницы"""
    page_title = _(u'Podarkoff-moscow - Магазин модной одежды и аксессуаров. Бесплатная доставка по России')
    products = Product.feautured.all()
    for p in products:
        try:
            p.image = ProductImage.objects.get(product=p, default=True)
        except Exception:
            p.image = "/media/products/images/none.png"

    bestseller = Product.bestseller.all()
    for b in bestseller:
        try:
            b.image = ProductImage.objects.get(product=b, default=True)
        except Exception:
            b.image = "/media/products/images/none.png"

    #Далее вывод новостей
    news = News.objects.all()[:5]
    # cart_items = cart.get_cart_items(request)
    # Функция locals получает все поля словаря
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

def category_view(request, category_slug, template_name="catalog/category.html"):
    """Представление для просмотра конкретной категории"""
    c = get_object_or_404(Category.active, slug=category_slug)
    products = c.product_set.all()
    for p in products:
        try:
            p.image_url = ProductImage.objects.get(product=p, default=True).url
        except Exception:
            p.image_url = "/media/products/images/none.png"
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

@csrf_protect
def product_view(request, product_slug, template_name="catalog/product.html"):
    """Представление для просмотра конкретного продукта"""
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.filter(is_active=True)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    try:
        product_image = ProductImage.objects.get(product=p, default=True)
        images = ProductImage.objects.filter(product=p)
    except Exception:
        print "Image for product #%s not found" % p.id
    characteristics = Characteristic.objects.filter(product=p)
    # Проверка HTTP метода
    if request.method == 'POST':
        # Добавление в корзину, создаем связанную форму
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        form2 = ProductOneClickForm(request.POST or None)

        # Проверка что отправляемые данные корректны
        if form.is_valid():
            # Добавляем в корзину и делаем перенаправление на страницу с корзиной
            cart.add_to_cart(request)
            # Если cookies работают, читаем их
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect('/product/%s' % product_slug)
        # if form2.is_valid():
        #     phone = request.POST['phone']
        #     text = u'Заявка на товар %s \n телефон: %s' % (page_title, phone)
        #     send_mail('в 1 клик', text, 'teamer777@gmail.com', ['greenteamer@bk.ru'], fail_silently=False)
        #     return HttpResponseRedirect('/product/%s/' % product_slug)

    else:
        # Если запрос GET, создаем не привязанную форму. request передаем в kwarg
        form = ProductAddToCartForm(request=request, label_suffix=':')
        form2 = ProductOneClickForm()
    # Присваиваем значению скрытого поля чистое имя продукта
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    form2.fields['product_name'].widget.attrs['value'] = p.name
    # Устанавливаем тестовые cookies при первом GET запросе
    request.session.set_test_cookie()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))
