# -*- coding: utf-8 -*-
import re
import json

from django.contrib.gis import forms
from django.contrib.gis.geos import LineString, Point
from django.utils.translation import ugettext_lazy as _

from allauth import app_settings
from allauth.account.utils import user_field

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


class SignupForm(forms.ModelForm):
    """
    This form will be wrapped by django-allauth. It will receive two password
    fields when user uses the standard signup view. In social signup, these
    password fields does not appear
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    country = forms.CharField(max_length=32)
    city = forms.CharField(max_length=32)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.populate_initial_fields_if_sociallogin(*args, **kwargs)

    def populate_initial_fields_if_sociallogin(self, *args, **kwargs):
        if hasattr(self, 'sociallogin'):
            user = self.sociallogin.user
            for key, field in self.fields.items():
                field.initial = getattr(user, key, '')
        return self

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.city = self.cleaned_data['city']
        user.country = self.cleaned_data['country']
        user.save()

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'country', 'city',)


class SignupBikeanjoForm(forms.ModelForm):
    gender = forms.CharField()
    birthday = forms.DateField()
    ride_experience = forms.ChoiceField(choices=models.BIKEANJO_EXPERIENCE)
    bike_use = forms.ChoiceField(choices=models.BIKE_USE)
    initiatives = forms.CharField(required=False, max_length=256)

    class Meta:
        model = models.User
        fields = ('gender', 'birthday', 'ride_experience', 'bike_use', 'initiatives')


class SignupRequesterForm(forms.ModelForm):
    gender = forms.CharField()
    birthday = forms.DateField()
    ride_experience = forms.ChoiceField(choices=models.REQUESTER_EXPERIENCE)

    class Meta:
        model = models.User
        fields = ('gender', 'birthday', 'ride_experience')


class HelpOfferForm(forms.ModelForm):
    help_with = forms.IntegerField()

    def get_help_choices(self):
        value = self.instance.help_with
        for code, label in models.HELP_OFFER:
            yield (code, label, bool(value & code))

    class Meta:
        model = models.User
        fields = ('help_with',)


class BikeanjoExperienceForm(forms.ModelForm):
    ride_experience = forms.ChoiceField(choices=models.BIKEANJO_EXPERIENCE)
    bike_use = forms.ChoiceField(choices=models.BIKE_USE)
    initiatives = forms.CharField(required=False, max_length=256)
    help_with = forms.IntegerField()

    def get_help_choices(self):
        value = self.instance.help_with
        for code, label in models.HELP_OFFER:
            yield (code, label, bool(value & code))

    class Meta:
        model = models.User
        fields = ('ride_experience', 'bike_use', 'initiatives', 'help_with',)


class HelpRequestForm(forms.ModelForm):
    help_with = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        requester = kwargs.pop('requester')
        super(HelpRequestForm, self).__init__(*args, **kwargs)
        self.instance.requester = requester

    def get_help_choices(self):
        for code, label in models.HELP_REQUEST:
            yield (code, label,)

    class Meta:
        model = models.HelpRequest
        fields = ('help_with',)


class HelpRequestUpdateForm(forms.ModelForm):
    requester_rating = forms.IntegerField(required=False)
    requester_eval = forms.CharField(required=False)

    def save(self, **kwargs):
        if self.instance.status == 'new':
            if 'status' in self.changed_data:
                self.instance.bikeanjo = None

        return super(HelpRequestUpdateForm, self).save(self, **kwargs)

    class Meta:
        model = models.HelpRequest
        fields = ('status', 'requester_eval', 'requester_rating',)


class RequestReplyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        helprequest = kwargs.pop('helprequest', None)

        super(RequestReplyForm, self).__init__(*args, **kwargs)

        self.instance.author = author
        self.instance.helprequest = helprequest

    class Meta:
        model = models.HelpReply
        fields = ('message',)


class PasswordResetForm(forms.Form):

    old_password = forms.CharField(label=_('Password'),
                                   widget=forms.PasswordInput, required=False)
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password (again)'),
                                widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        if not self.instance.has_usable_password() or\
           self.instance.check_password(old_password):
            return old_password

        raise forms.ValidationError('A senha antiga está incorreta.')

    def clean_password1(self):
        pass1 = self.cleaned_data.get('password1')

        if self.instance.has_usable_password() and\
           self.instance.check_password(pass1):
            raise forms.ValidationError('A nova senha é igual a antiga')

        return pass1

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')

        if pass1 == pass2:
            return pass1

        raise forms.ValidationError('As senhas devem ser iguais')

    def save(self, **kwargs):
        password = self.cleaned_data.get('password2')
        self.instance.set_password(password)
        self.instance.save()
        return self.instance
