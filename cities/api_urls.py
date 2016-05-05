# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from cities import views

router = routers.DefaultRouter()
router.register(r'countries', views.CountryViewSet)
router.register(r'countryalias', views.CountryAliasViewSet)
router.register(r'states', views.StateViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'cityalias', views.CityAliasViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^ac/country', views.CountryAutocompleteView.as_view(), name='ac_country'),
    url(r'^ac/city', views.CityAutocompleteView.as_view(), name='ac_city'),
]
