# -*- coding: utf-8 -*-
from django import forms
from models import GENDER, CYCLIST_ROLES


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    role = forms.ChoiceField(choices=CYCLIST_ROLES)
    bio = forms.CharField(max_length=140, required=False)
    date_of_birth = forms.DateField(input_formats=['%d/%m/%Y'], required=False)
    gender = forms.ChoiceField(choices=GENDER, required=False)
    phone = forms.CharField(max_length=32, required=False)
    years_experience = forms.IntegerField(min_value=0, required=False)
    address = forms.CharField(max_length=64, required=False)
    address_number = forms.IntegerField(min_value=0, required=False)
    address_complement = forms.CharField(max_length=16, required=False)
    locality = forms.CharField(max_length=32, required=False)
    state = forms.CharField(max_length=32, required=False)
    level_in_mechanics = forms.IntegerField(min_value=0, max_value=5,required=False)
    level_in_security = forms.IntegerField(min_value=0, max_value=5, required=False)
    level_in_legislation = forms.IntegerField(min_value=0, max_value=5, required=False)
    level_in_routes = forms.IntegerField(min_value=0, max_value=5, required=False)
    services = forms.CharField(max_length=64, required=False)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        user.cyclist.role = self.cleaned_data['role']
        user.cyclist.bio = self.cleaned_data['bio']
        user.cyclist.date_of_birth = self.cleaned_data['date_of_birth']
        user.cyclist.gender = self.cleaned_data['gender']
        user.cyclist.phone = self.cleaned_data['phone']
        user.cyclist.years_experience = self.cleaned_data['years_experience']
        user.cyclist.address = self.cleaned_data['address']
        user.cyclist.address_number = self.cleaned_data['address_number']
        user.cyclist.address_complement = self.cleaned_data['address_complement']
        user.cyclist.locality = self.cleaned_data['locality']
        user.cyclist.state = self.cleaned_data['state']
        user.cyclist.level_in_mechanics = self.cleaned_data['level_in_mechanics']
        user.cyclist.level_in_security = self.cleaned_data['level_in_security']
        user.cyclist.level_in_legislation = self.cleaned_data['level_in_legislation']
        user.cyclist.level_in_routes = self.cleaned_data['level_in_routes']
        user.cyclist.services = self.cleaned_data['services']
        user.cyclist.save()
