# -*- coding: utf-8 -*-
import django_filters
from rest_framework import viewsets
from serializers import CountrySerializer, StateSerializer, CitySerializer, CityAliasSerializer, CountryAliasSerializer
from models import Country, CountryAlias, State, City, CityAlias
from rest_framework import filters
from dal import autocomplete

class CountryFilter(filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_type='lowermatch')
    alias = django_filters.CharFilter(name="countryalias__name", lookup_type='lowermatch')

    class Meta:
        model = Country
        fields = ('id', 'name', 'acronym',)


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_class = CountryFilter

    def get_queryset(self):
        qs = super(CountryViewSet, self).get_queryset()
        return qs.distinct()


#
# django_filters for CoutryAliasViewSet
#
class CountryAliasFilter(filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_type='lowermatch')

    class Meta:
        model = CountryAlias
        fields = ('id', 'name', 'country', 'country__name', 'country__acronym',)


class CountryAliasViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CountryAliasFilter

    queryset = CountryAlias.objects.all()\
        .select_related('country')
    serializer_class = CountryAliasSerializer

    def get_queryset(self):
        qs = super(CountryAliasViewSet, self).get_queryset()

        if 'name' in self.request.REQUEST:
            value = self.request.REQUEST.get('name', '')
            field = '"%s"."name"' % CountryAlias._meta.db_table
            function = 'levenshtein(%s, %s)' % ("%s", field)
            qs = qs.extra(
                select={'weight': function, },
                select_params=(value,)
            ).distinct().order_by('weight')
        return qs


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


#
# django_filters for CityViewSet
#
class CityFilter(filters.FilterSet):
    alias = django_filters.CharFilter(name="cityalias__name", lookup_type='lowermatch')

    class Meta:
        model = City
        fields = ('id', 'name', 'country__acronym', 'alias',)


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
            ).distinct().order_by('weight')
        return qs


#
# django_filters for CityViewSet
#
class CityAliasFilter(filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_type='lowermatch')

    class Meta:
        model = CityAlias
        fields = ('id', 'name', 'city__name', 'city__country',
                  'city__country__acronym',)


class CityAliasViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CityAliasFilter

    queryset = CityAlias.objects.all()\
        .select_related('city', 'city__country')\
        .order_by('city__name')
    serializer_class = CityAliasSerializer

    def get_queryset(self):
        qs = super(CityAliasViewSet, self).get_queryset()

        if 'name' in self.request.REQUEST:
            value = self.request.REQUEST.get('name', '')
            field = '"%s"."name"' % CityAlias._meta.db_table
            function = 'levenshtein(%s, %s)' % ("%s", field)
            qs = qs.extra(
                select={'weight': function, },
                select_params=(value,)
            ).distinct().order_by('weight')
        return qs


# 
# django-autocomplete-light for admin
# 
class CountryAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Country.objects.all()
        if self.q:
            qs = qs.filter(name__lowermatch=self.q)
        return qs


class CityAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()
        if self.q:
            qs = qs.filter(name__lowermatch=self.q)
        return qs
