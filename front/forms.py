# -*- coding: utf-8 -*-
import re
import json

from django.contrib.gis import forms
from django.contrib.gis.geos import LineString, Point

import models


class TrackForm(forms.Form):
    tracks = forms.CharField(widget=forms.HiddenInput(attrs={'bikeanjo-geojson': 'lines'}),
                             required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TrackForm, self).__init__(*args, **kwargs)

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

    def save(self):
            for track in self.cleaned_data['tracks']:
                track.user = self.user
                track.save()
            return self.cleaned_data['tracks']


class TrackReviewForm(TrackForm):

    def __init__(self, *args, **kwargs):
        super(TrackReviewForm, self).__init__(*args, **kwargs)
        self['tracks'].field.initial = self.load_tracks()

    def load_tracks(self):
        tracks = models.Track.objects.filter(user=self.user)
        return json.dumps([t.json() for t in tracks])

    def save(self):
        tracks = super(TrackReviewForm, self).save()
        do_no_delete = (t.id for t in tracks)
        models.Track.objects\
            .filter(user=self.user)\
            .exclude(id__in=do_no_delete)\
            .delete()
        return tracks


class PointsForm(forms.Form):
    points = forms.CharField(widget=forms.HiddenInput(attrs={'bikeanjo-geojson': 'points'}),
                             required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PointsForm, self).__init__(*args, **kwargs)
        self['points'].field.initial = self.load_points()

    def clean_points(self):
        if not self.cleaned_data.get('points'):
            return []

        try:
            json_points = json.loads(self.cleaned_data.get('points'))
            points = []

            for p in json_points:
                _id = p.get('properties').get('id')

                if _id:
                    point = models.Point.objects.get(id=_id)
                else:
                    point = models.Point()

                point.coords = Point(p.get('coordinates'))
                point.address = p.get('properties').get('address')

                points.append(point)

            return points
        except ValueError, e:
            raise forms.ValidationError(e.message)

    def save(self):
        for point in self.cleaned_data['points']:
            point.user = self.user
            point.save()
        return self.cleaned_data['points']

    def load_points(self):
        points = models.Point.objects.filter(user=self.user)
        return json.dumps([p.json() for p in points])


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


class SignupVolunteerForm(forms.ModelForm):
    gender = forms.CharField()
    birthday = forms.DateField()
    ride_experience = forms.ChoiceField(choices=models.VOLUNTEER_EXPERIENCE)
    bike_use = forms.ChoiceField(choices=models.BIKE_USE)
    initiatives = forms.CharField(required=False, max_length=256)

    class Meta:
        model = models.Cyclist
        fields = ('gender', 'birthday', 'ride_experience', 'bike_use', 'initiatives')


class SignupRequesterForm(forms.ModelForm):
    gender = forms.CharField()
    birthday = forms.DateField()
    ride_experience = forms.ChoiceField(choices=models.REQUESTER_EXPERIENCE)

    class Meta:
        model = models.Cyclist
        fields = ('gender', 'birthday', 'ride_experience')


class HelpOfferForm(forms.ModelForm):
    help_with = forms.IntegerField()

    def get_help_choices(self):
        value = self.instance.help_with
        for code, label in models.HELP_OFFER:
            yield (code, label, bool(value & code))

    class Meta:
        model = models.Cyclist
        fields = ('help_with',)


class HelpRequestForm(forms.ModelForm):
    help_with = forms.IntegerField()

    def get_help_choices(self):
        value = self.instance.help_with
        for code, label in models.HELP_REQUEST:
            yield (code, label, bool(value & code))

    class Meta:
        model = models.Cyclist
        fields = ('help_with',)
