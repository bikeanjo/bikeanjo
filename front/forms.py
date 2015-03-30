# -*- coding: utf-8 -*-
from django import forms
from models import CYCLIST_ROLES, GENDER, HELP_WITH


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    birthday = forms.DateField(required=False)
    city = forms.CharField(max_length=32, required=False)
    country = forms.CharField(max_length=32, required=False)
    gender = forms.ChoiceField(choices=GENDER, required=False)
    help_with = forms.ChoiceField(choices=HELP_WITH)
    phone = forms.CharField(max_length=32, required=False)
    role = forms.ChoiceField(choices=CYCLIST_ROLES)
    state = forms.CharField(max_length=32, required=False)

    def __init__(self, *argz, **kwargz):
        super(SignupForm, self).__init__(*argz, **kwargz)

        if hasattr(self, 'sociallogin'):
            extra = self.sociallogin.account.extra_data
            self['birthday'].value = extra.get('birthday', '')

            if extra.get('gender') == 'male':
                self['gender'].value = 'M'
            elif extra.get('gender') == 'female':
                self['gender'].value = 'F'

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        cyclist = user.cyclist

        cyclist.birthday = self.cleaned_data['birthday']
        cyclist.city = self.cleaned_data['city']
        cyclist.country = self.cleaned_data['country']
        cyclist.gender = self.cleaned_data['gender']
        cyclist.help_with = self.cleaned_data['help_with']
        cyclist.phone = self.cleaned_data['phone']
        cyclist.role = self.cleaned_data['role']
        cyclist.state = self.cleaned_data['state']
        cyclist.save()
