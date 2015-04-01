# -*- coding: utf-8 -*-
import re
from django.contrib.gis import forms

import models


class TrackForm(forms.Form):
    json_points = forms.CharField(widget=forms.HiddenInput)


class SignupForm(forms.Form):
    """
    This form will be wrapped by django-allauth. It will receive two password
    fields when user uses the standard signup view. In social signup, these
    password fields does not appear
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    birthday = forms.DateField(required=False)
    city = forms.CharField(max_length=32, required=False)
    country = forms.CharField(max_length=32, required=False)
    gender = forms.ChoiceField(choices=models.GENDER, required=False)
    help_with = forms.ChoiceField(choices=models.HELP_WITH)
    phone = forms.CharField(max_length=32, required=False)
    role = forms.ChoiceField(choices=models.CYCLIST_ROLES)
    state = forms.CharField(max_length=32, required=False)

    def __init__(self, *argz, **kwargz):
        super(SignupForm, self).__init__(*argz, **kwargz)

        if hasattr(self, 'sociallogin'):
            extra = self.sociallogin.account.extra_data

            # facebook birthday is month/day/year
            match = re.match('^(\d\d)/(\d\d)/(\d\d\d\d)$', extra.get('birthday'))
            if match:
                self['birthday'].value = '{1}/{0}/{2}'.format(*match.groups())

            if extra.get('gender') == 'male':
                self['gender'].value = 'M'
            elif extra.get('gender') == 'female':
                self['gender'].value = 'F'

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        cyclist = models.Cyclist()
        cyclist.user = user
        cyclist.birthday = self.cleaned_data['birthday']
        cyclist.city = self.cleaned_data['city']
        cyclist.country = self.cleaned_data['country']
        cyclist.gender = self.cleaned_data['gender']
        cyclist.help_with = self.cleaned_data['help_with']
        cyclist.phone = self.cleaned_data['phone']
        cyclist.role = self.cleaned_data['role']
        cyclist.state = self.cleaned_data['state']
        cyclist.save()
