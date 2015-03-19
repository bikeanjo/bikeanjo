# -*- coding: utf-8 -*-
from django import forms
from models import GENDER, CYCLIST_ROLES


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    role = forms.ChoiceField(choices=CYCLIST_ROLES)
    bio = forms.CharField(max_length=140, required=False)
    date_of_birth = forms.DateField(required=False)
    gender = forms.ChoiceField(choices=GENDER, required=False)
    phone = forms.CharField(max_length=32, required=False)
    years_experience = forms.IntegerField(min_value=0, required=False)
    address = forms.CharField(max_length=64, required=False)
    address_number = forms.IntegerField(min_value=0, required=False)
    address_complement = forms.CharField(max_length=16, required=False)
    locality = forms.CharField(max_length=32, required=False)
    state = forms.CharField(max_length=32, required=False)
    level_in_mechanics = forms.IntegerField(min_value=0, max_value=5,
                                            required=False)
    level_in_security = forms.IntegerField(min_value=0, max_value=5,
                                           required=False)
    level_in_legislation = forms.IntegerField(min_value=0, max_value=5,
                                              required=False)
    level_in_routes = forms.IntegerField(min_value=0, max_value=5,
                                         required=False)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # abrevia nome pra nao falhar no flake
        cyc = user.cyclist

        cyc.role = self.cleaned_data['role']
        cyc.bio = self.cleaned_data['bio']
        cyc.date_of_birth = self.cleaned_data['date_of_birth']
        cyc.gender = self.cleaned_data['gender']
        cyc.phone = self.cleaned_data['phone']
        cyc.years_experience = self.cleaned_data['years_experience']
        cyc.address = self.cleaned_data['address']
        cyc.address_number = self.cleaned_data['address_number']
        cyc.address_complement = self.cleaned_data['address_complement']
        cyc.locality = self.cleaned_data['locality']
        cyc.state = self.cleaned_data['state']
        cyc.level_in_mechanics = self.cleaned_data['level_in_mechanics']
        cyc.level_in_security = self.cleaned_data['level_in_security']
        cyc.level_in_legislation = self.cleaned_data['level_in_legislation']
        cyc.level_in_routes = self.cleaned_data['level_in_routes']
        cyc.save()
