# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from serializers import CountrySerializer, StateSerializer, CitySerializer
from models import Country, State, City
from rest_framework import filters


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'name', 'state__acronym', 'state__country',
                     'state__country__name',)

    queryset = City.objects.all()\
        .select_related('state')\
        .order_by('name')
    serializer_class = CitySerializer
