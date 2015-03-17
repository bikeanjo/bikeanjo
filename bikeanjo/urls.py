# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin

from front.views import HomeView
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'poneybike.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
]
