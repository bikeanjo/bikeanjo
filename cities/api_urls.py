# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from cities import api_views as views

router = routers.DefaultRouter()
router.register(r'countries', views.CountryViewSet)
router.register(r'states', views.StateViewSet)
router.register(r'cities', views.CityViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
