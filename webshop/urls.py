# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.conf.urls import patterns, include, url
from django.contrib import admin

from webshop import settings
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^webshop/', include('webshop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin_tools/', include('admin_tools.urls')),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # General application URLs
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('webshop.accounts.urls')),
    url(r'^', include('webshop.catalog.urls')),
    url(r'^cart/', include('webshop.cart.urls')),
    url(r'^checkout/', include('webshop.checkout.urls')),
    url(r'^', include('webshop.news.urls')),
    url(r'^search/', include('webshop.search.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),

    # enable language choice
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^set_language/$', 'django.views.i18n.set_language', name='set_language'),

    # урл для robokassa
    url(r'^robokassa/', include('robokassa.urls')),
    # url(r'^robokassa/result/', include('webshop.checkout.robokassa_urls')),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
        # if work then show 404 Directory indexes are not allowed here.
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
        )

handler404 = 'webshop.views.file_not_found_404'
