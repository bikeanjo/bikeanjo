# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import Country, State, City


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'acronym', 'name', 'url',)


class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'acronym', 'country', 'name', 'url',)


class CitySerializer(serializers.HyperlinkedModelSerializer):
    state_acronym = serializers.CharField(
        source='state.acronym',
        read_only=True
    )

    class Meta:
        model = City
        fields = ('id', 'name', 'state_acronym')
