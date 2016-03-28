# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import Country, CountryAlias, State, City, CityAlias


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'acronym', 'name', 'url',)


class CountryAliasSerializer(serializers.HyperlinkedModelSerializer):
    country_acronym = serializers.CharField(
        source='country.acronym',
        read_only=True
    )

    country_id = serializers.IntegerField(
        source='country.id',
        read_only=True
    )

    country_name = serializers.CharField(
        source='country.name',
        read_only=True
    )

    class Meta:
        model = CountryAlias
        fields = ('id', 'name', 'country_id', 'country_name', 'country_acronym',)


class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'acronym', 'country', 'name', 'url',)


class CitySerializer(serializers.HyperlinkedModelSerializer):
    state_acronym = serializers.CharField(
        source='state.acronym',
        read_only=True
    )
    country_acronym = serializers.CharField(
        source='country.acronym',
        read_only=True
    )

    class Meta:
        model = City
        fields = ('id', 'name', 'state_acronym', 'country_acronym',)


class CityAliasSerializer(serializers.HyperlinkedModelSerializer):
    country_acronym = serializers.CharField(
        source='city.country.acronym',
        read_only=True
    )

    city_id = serializers.IntegerField(
        source='city.id',
        read_only=True
    )

    city_name = serializers.CharField(
        source='city.name',
        read_only=True
    )

    class Meta:
        model = CityAlias
        fields = ('id', 'name', 'city_id', 'city_name', 'country_acronym',)
