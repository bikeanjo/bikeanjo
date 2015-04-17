# -*- coding: utf-8 -*-
import re
import json

from django.contrib.gis import forms
from django.contrib.gis.geos import LineString, Point

import models


class TrackForm(forms.Form):
    json_points = forms.CharField(widget=forms.HiddenInput)

    def clean_json_points(self):
        try:
            return json.loads(self.cleaned_data['json_points'])
        except ValueError, e:
            raise forms.ValidationError(e.message)

    def save(self, cyclist):
        points = self.cleaned_data['json_points']
        track = models.Track(cyclist=cyclist)

        start = Point(
            points['start']['coords']['lon'],
            points['start']['coords']['lat'],
        )
        end = Point(
            points['end']['coords']['lon'],
            points['end']['coords']['lat'],
        )

        track.track = LineString(start, end)
        track.start = points['start']['address']
        track.end = points['end']['address']

        track.save()


class SignupForm(forms.Form):
    """
    This form will be wrapped by django-allauth. It will receive two password
    fields when user uses the standard signup view. In social signup, these
    password fields does not appear
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    country = forms.CharField(max_length=32, required=False)
    city = forms.CharField(max_length=32, required=False)

    def __init__(self, *argz, **kwargz):
        super(SignupForm, self).__init__(*argz, **kwargz)

        if hasattr(self, 'sociallogin'):
            extra = self.sociallogin.account.extra_data

            # facebook birthday is month/day/year
            match = re.match('^(\d\d)/(\d\d)/(\d\d\d\d)$', extra.get('birthday'))
            if match:
                self['birthday'].value = '{1}/{0}/{2}'.format(*match.groups())

            self['gender'].value = extra.get('gender')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        cyclist = models.Cyclist()
        cyclist.user = user
        cyclist.city = self.cleaned_data['city']
        cyclist.country = self.cleaned_data['country']
        cyclist.save()

        user.cyclist = cyclist


class SignupCompleteForm(forms.ModelForm):
    gender = forms.CharField()
    birthday = forms.DateField()
    ride_experience = forms.ChoiceField(choices=models.EXPERIENCE)
    bike_use = forms.ChoiceField(choices=models.BIKE_USE)
    initiatives = forms.CharField(required=False, max_length=256)

    class Meta:
        model = models.Cyclist
        fields = ('gender', 'birthday', 'ride_experience', 'bike_use', 'initiatives')
