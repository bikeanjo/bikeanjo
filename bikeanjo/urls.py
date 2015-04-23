# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

import front.views

admin.autodiscover()

urlpatterns = [
    # the django admin
    url(r'^admin/', include(admin.site.urls)),

    # django allauth
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/signup/$', front.views.SignupView.as_view()),
    url(r'^accounts/', include('allauth.urls')),

    # bikeanjo urls
    url(r'^$', front.views.HomeView.as_view(), name='home'),

    url(r'^(?P<role>volunteer|requester)/signup/$',
        front.views.SignupView.as_view(), name='cyclist_account_signup'),
    url(r'^(?P<role>volunteer|requester)/signup/complete/$',
        front.views.SignupCompleteView.as_view(), name='cyclist_account_signup_complete'),
    url(r'^volunteer/help-offer/$',
        front.views.HelpOfferView.as_view(), name='volunteer_help_offer'),
    url(r'^volunteer/register-routes-to-help/$',
        front.views.TrackRegisterView.as_view(), name='volunteer_register_routes'),
    url(r'^volunteer/registered-routes/$',
        front.views.TrackListView.as_view(), name='volunteer_registered_routes'),



    url(r'^login/$', TemplateView.as_view(template_name="login.html")),
    url(r'^solicitante/$', TemplateView.as_view(template_name="dashboard_solicitante.html")),
]
