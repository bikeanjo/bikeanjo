# -*- coding: utf-8 -*-
import re
import json

from django.contrib.gis import forms
from django.contrib.gis.geos import LineString, Point

import models


class TrackForm(forms.Form):
    tracks = forms.CharField(widget=forms.HiddenInput(attrs={'bikeanjo-geojson': 'lines'}),
                             required=False)

    def clean_tracks(self):
        if not self.cleaned_data.get('tracks'):
            return []

        try:
            lines = json.loads(self.cleaned_data.get('tracks'))
            tracks = []

            for line in lines:
                _id = line.get('properties').get('id')

                if _id:
                    track = models.Track.objects.get(id=_id)
                else:
                    track = models.Track()

                track.track = LineString([c for c in line.get('coordinates')])
                track.start = line.get('properties').get('start')
                track.end = line.get('properties').get('end')

                tracks.append(track)

            return tracks
        except ValueError, e:
            raise forms.ValidationError(e.message)

    def save(self, cyclist):
            for track in self.cleaned_data['tracks']:
                track.cyclist = cyclist
                track.save()
            return self.cleaned_data['tracks']


class TrackReviewForm(TrackForm):

    def __init__(self, *args, **kwargs):
        self.cyclist = kwargs.pop('cyclist', None)
        super(TrackReviewForm, self).__init__(*args, **kwargs)
        self['tracks'].field.initial = self.load_tracks()

    def load_tracks(self):
        tracks = models.Track.objects.filter(cyclist=self.cyclist)
        return json.dumps([t.json() for t in tracks])

    def save(self, cyclist):
        tracks = super(TrackReviewForm, self).save(cyclist=cyclist)
        do_no_delete = (t.id for t in tracks)
        models.Track.objects\
            .filter(cyclist=cyclist)\
            .exclude(id__in=do_no_delete)\
            .delete()
        return tracks


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


class HelpOfferForm(forms.ModelForm):
    help_with = forms.IntegerField()

    def get_help_choices(self):
        value = self.instance.help_with
        for code, label in models.HELP:
            yield (code, label, bool(value & code))

    class Meta:
        model = models.Cyclist
        fields = ('help_with',)
