# -*- coding: utf-8 -*-
import re
import json

from django.contrib.gis import forms
from django.contrib.gis.geos import LineString, Point
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from allauth import app_settings
from allauth.account.utils import user_field

from cities.models import Country
import models


class TrackForm(forms.Form):
    tracks = forms.CharField(label=_('Tracks'),
                             widget=forms.HiddenInput(attrs={'bikeanjo-geojson': 'lines'}),
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
        return '[%s]' % ','.join([t.json() for t in tracks])

    def save(self):
        tracks = super(TrackReviewForm, self).save()
        do_no_delete = (t.id for t in tracks)
        models.Track.objects\
            .filter(user=self.user)\
            .exclude(id__in=do_no_delete)\
            .delete()
        return tracks


class PointsForm(forms.Form):
    points = forms.CharField(label=_('Points'),
                             widget=forms.HiddenInput(attrs={'bikeanjo-geojson': 'points'}),
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
        return '[%s]' % ','.join([p.json() for p in points])


class SignupForm(forms.ModelForm):
    """
    This form will be wrapped by django-allauth. It will receive two password
    fields when user uses the standard signup view. In social signup, these
    password fields does not appear
    """
    full_name = forms.CharField(label=_('Full name'), max_length=60)
    email2 = forms.CharField(label=_('E-mail (again)'))
    country = forms.CharField(label=_('Country'), max_length=32)
    city = forms.CharField(label=_('City'), max_length=32)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.populate_initial_fields_if_sociallogin(*args, **kwargs)

    def populate_initial_fields_if_sociallogin(self, *args, **kwargs):
        if hasattr(self, 'sociallogin'):
            user = self.sociallogin.user
            for key, field in self.fields.items():
                field.initial = getattr(user, key, '')
            self.fields['full_name'].initial = user.get_full_name()
            self.fields['email2'].initial = user.email
        return self

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email != email2:
            raise forms.ValidationError(_('The informed emails are different.'))
        return email

    def signup(self, request, user):
        full_name = self.cleaned_data['full_name'].split(' ')
        user.first_name = full_name[0]
        user.last_name = ' '.join(full_name[1:])

        user.city = self.cleaned_data['city']
        user.country = self.cleaned_data['country']
        user.save()

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'country', 'city',)


class SignupBikeanjoForm(forms.ModelForm):
    gender = forms.CharField(label=_('Gender'))
    birthday = forms.DateField(label=_('Birthday'))
    ride_experience = forms.ChoiceField(label=_('Ride experience'), choices=models.BIKEANJO_EXPERIENCE)
    bike_use = forms.ChoiceField(label=_('Bike user'), choices=models.BIKE_USE)
    initiatives = forms.CharField(label=_('Initiatives'), required=False, max_length=256)

    class Meta:
        model = models.User
        fields = ('gender', 'birthday', 'ride_experience', 'bike_use', 'initiatives')


class SignupRequesterForm(forms.ModelForm):
    gender = forms.CharField(label=_('Gender'))
    birthday = forms.DateField(label=_('Birthday'))
    ride_experience = forms.ChoiceField(choices=models.REQUESTER_EXPERIENCE)

    class Meta:
        model = models.User
        fields = ('gender', 'birthday', 'ride_experience')


class HelpOfferForm(forms.ModelForm):
    help_with = forms.IntegerField(label=_('Help with'))

    def get_help_choices(self):
        value = self.instance.help_with
        for code, label in models.HELP_OFFER:
            yield (code, label, bool(value & code))

    class Meta:
        model = models.User
        fields = ('help_with',)


class BikeanjoExperienceForm(forms.ModelForm):
    ride_experience = forms.ChoiceField(label=_('Ride experience'), choices=models.BIKEANJO_EXPERIENCE)
    bike_use = forms.ChoiceField(label=_('Bike use'), choices=models.BIKE_USE)
    initiatives = forms.CharField(label=_('Initiatives'), required=False, max_length=256)
    help_with = forms.IntegerField(label=_('Help with'))

    def get_help_choices(self):
        value = self.instance.help_with
        for code, label in models.HELP_OFFER:
            yield (code, label, bool(value & code))

    class Meta:
        model = models.User
        fields = ('ride_experience', 'bike_use', 'initiatives', 'help_with',)


class BikeanjoUserInforForm(forms.ModelForm):
    class Meta:
        fields = ('avatar', 'first_name', 'last_name', 'email', 'country',
                  'city', 'gender', 'birthday', 'available',)
        model = models.User


class RequesterUserInforForm(forms.ModelForm):
    ride_experience = forms.ChoiceField(label=_('Ride experience'), choices=models.REQUESTER_EXPERIENCE)
    bike_use = forms.ChoiceField(label=_('Bike user'), choices=models.BIKE_USE)

    class Meta:
        fields = ('avatar', 'first_name', 'last_name', 'email', 'country', 'city', 'gender', 'birthday',
                  'ride_experience', 'bike_use', 'initiatives',)
        model = models.User


class HelpRequestForm(forms.ModelForm):
    help_with = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        requester = kwargs.pop('requester')
        super(HelpRequestForm, self).__init__(*args, **kwargs)
        self.instance.requester = requester

        if not requester.accepted_agreement:
            last_request = requester.helprequested_set.first()

            if last_request:
                self.instance = last_request

    def get_help_choices(self):
        for code, label in models.HELP_REQUEST:
            yield (code, label,)

    class Meta:
        model = models.HelpRequest
        fields = ('help_with',)


class HelpRequestRouteForm(forms.ModelForm):
    track = forms.CharField(label=_('Track'),
                            widget=forms.HiddenInput(attrs={'bikeanjo-geojson': 'lines'}),
                            required=False)

    def __init__(self, *args, **kwargs):
        super(HelpRequestRouteForm, self).__init__(*args, **kwargs)
        self._original_track = self.instance.track

    def clean_track(self):
        track = self._original_track
        try:
            lines = json.loads(self.cleaned_data.get('track'))
            if type(lines) in (list, tuple) and len(lines) > 0:
                track = track or models.Track()
                line = lines[0]
                track.user = self.instance.requester
                track.track = LineString([c for c in line.get('coordinates')])
                track.start = line.get('properties').get('start')
                track.end = line.get('properties').get('end')
                track.save()
        except ValueError, e:
            raise forms.ValidationError(e.message)
        return track

    class Meta:
        model = models.HelpRequest
        fields = ('track',)


class HelpRequestPointForm(forms.Form):
    points = forms.CharField(label=_('Points'),
                             widget=forms.HiddenInput(attrs={'bikeanjo-geojson': 'points'}),
                             required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super(HelpRequestPointForm, self).__init__(*args, **kwargs)
        self['points'].field.initial = self.load_points()

    def clean_points(self):
        try:
            points = []
            json_points = json.loads(self.cleaned_data.get('points'))
            if type(json_points) in (list, tuple) and len(json_points) > 0:
                for json_p in json_points:
                    point = models.Point()
                    point.coords = Point(json_p.get('coordinates'))
                    point.address = json_p.get('properties').get('address')
                    point.id = json_p.get('properties').get('id', None)
                    points.append(point)
            return points
        except ValueError, e:
            raise forms.ValidationError(e.message)
        return []

    def save(self):
        points = self.cleaned_data['points']

        models.Point.objects\
            .exclude(id__in=[p.id for p in points if p.id])\
            .delete()

        for point in points:
            if not point.id:
                point.user = self.instance.requester
                point.helprequest = self.instance
                point.save()

        return self.instance

    def load_points(self):
        points = models.Point.objects.filter(helprequest=self.instance)
        return '[%s]' % ','.join([p.json() for p in points])


class HelpRequestUpdateForm(forms.ModelForm):
    requester_rating = forms.IntegerField(label=_('Requester rating'), required=False)
    requester_eval = forms.CharField(label=_('Requester evaluation'), required=False)
    reason = forms.CharField(label=_('Reason'), widget=forms.HiddenInput, required=False)

    def save(self, **kwargs):
        data = self.cleaned_data
        req = self.instance

        if 'status' in self.changed_data and req.status in ['new', 'canceled']:
            if req.bikeanjo:
                match, created = req.match_set.get_or_create(bikeanjo_id=req.bikeanjo)
                match.rejected_date = now()
                match.reason = data.get('reason', 'user canceled request')
                match.save()
            req.bikeanjo = None

        return super(HelpRequestUpdateForm, self).save(self, **kwargs)

    class Meta:
        model = models.HelpRequest
        fields = ('status', 'requester_eval', 'requester_rating',)


class BikeanjoAcceptRequestForm(forms.ModelForm):
    reason = forms.CharField(label=_('Reason'), widget=forms.HiddenInput, required=False)

    def save(self, **kwargs):
        data = self.cleaned_data
        req = self.instance

        if req.status == 'new':
            if req.bikeanjo:
                match, created = req.match_set.get_or_create(bikeanjo_id=req.bikeanjo)
                match.rejected_date = now()
                match.reason = data.get('reason')
                match.save()
            req.bikeanjo = None

        return super(BikeanjoAcceptRequestForm, self).save(self, **kwargs)

    class Meta:
        model = models.HelpRequest
        fields = ('status',)


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


class SignupAgreementForm(forms.ModelForm):
    check1 = forms.BooleanField()
    check2 = forms.BooleanField()
    check3 = forms.BooleanField()
    accepted_agreement = forms.BooleanField()
    message = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(SignupAgreementForm, self).clean()
        msg = 'Você deve aceitar os termos para usar o site'
        for field, value in cleaned_data.items():
            if field != 'message' and not value:
                self.add_error(field, msg)

    def save(self, **kwargs):
        super(SignupAgreementForm, self).save(**kwargs)

        message = self.cleaned_data.get('message', '')
        if message and self.instance.role == 'requester':
            helprequest = self.instance.helprequested_set.first()
            if helprequest:
                helprequest.helpreply_set.create(
                    message=message,
                    author=self.instance)

    class Meta:
        model = models.User
        fields = ('accepted_agreement',)


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author', None)
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.instance.author = author

    class Meta:
        model = models.Feedback
        fields = ('message',)
