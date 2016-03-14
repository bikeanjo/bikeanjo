# -*- coding: utf-8 -*-
import django_filters
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


class CityFilter(filters.FilterSet):
    alias = django_filters.CharFilter(name="cityalias__alias", lookup_type='startswith')

    class Meta:
        model = City
        fields = ('id', 'name', 'state__acronym', 'country',
                  'country__name', 'country__acronym', 'alias',)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CityFilter

    queryset = City.objects.all()\
        .select_related('state', 'country')\
        .order_by('name') \
        .distinct()
    serializer_class = CitySerializer

    def get_queryset(self):
        qs = super(CityViewSet, self).get_queryset()

        if 'alias' in self.request.REQUEST:
            value = self.request.REQUEST.get('alias', '')
            field = '"%s"."name"' % City._meta.db_table
            function = 'levenshtein(%s, %s)' % ("%s", field)
            qs = qs.extra(
                select={'weight': function, },
                select_params=(value,)
            ).order_by('weight')
        return qs
