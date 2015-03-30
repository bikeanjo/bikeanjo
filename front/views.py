# -*- coding: utf-8 -*-
from django.views.generic import FormView, TemplateView

import allauth.account.views
import forms


class SignupView(allauth.account.views.SignupView):

    def get_form_kwargs(self):
        kwargs = super(SignupView, self).get_form_kwargs()
        if self.request.method == 'GET':
            kwargs['initial'].update(self.request.GET.dict())
        return kwargs


class HelpOfferView(TemplateView):
    template_name = 'help_offer.html'


class HomeView(TemplateView):
    template_name = 'home.html'
