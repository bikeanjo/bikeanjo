# -*- coding: utf-8 -*-
from django.views.generic import FormView, TemplateView
from django.forms.formsets import formset_factory

import allauth.account.views
import forms


class SignupView(allauth.account.views.SignupView):

    def get_form_kwargs(self):
        kwargs = super(SignupView, self).get_form_kwargs()
        if self.request.method == 'GET':
            kwargs['initial'].update(self.request.GET.dict())
        return kwargs


class TrackView(FormView):
    template_name = 'routes_form.html'
    form_class = forms.TrackForm
    success_url = '/'

    def form_valid(self, form):
        form.save(cyclist=self.request.user.cyclist)
        return super(TrackView, self).form_valid(form)


class HomeView(TemplateView):
    template_name = 'home.html'
