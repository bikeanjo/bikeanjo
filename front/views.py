# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.views.generic import FormView, TemplateView

import allauth.account.views
import forms


def firstof(*args):
    for arg in args:
        if arg:
            return arg


class SignupView(allauth.account.views.SignupView):
    def get_success_url(self):
        if self.kwargs.get('role') == 'volunteer':
            return reverse('volunteer_account_signup_complete')
        return reverse('requester_account_signup_complete')

    def form_valid(self, form):
        response = super(SignupView, self).form_valid(form)
        self.request.user.cyclist.role = self.kwargs.get('role')
        self.request.user.cyclist.save()
        return response


class SignupVolunteerView(LoginRequiredMixin, FormView):
    form_class = forms.SignupVolunteerForm
    template_name = 'bikeanjo_complete_signup.html'

    def get_success_url(self):
        return reverse('volunteer_help_offer')

    def get_form_kwargs(self):
        kwargs = super(SignupVolunteerView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user.cyclist
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(SignupVolunteerView, self).form_valid(form)


class SignupRequesterView(LoginRequiredMixin, FormView):
    form_class = forms.SignupRequesterForm
    template_name = 'requester_complete_signup.html'

    def get_success_url(self):
        return reverse('requester_help_request')

    def get_form_kwargs(self):
        kwargs = super(SignupRequesterView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user.cyclist
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(SignupRequesterView, self).form_valid(form)


class HelpOfferView(LoginRequiredMixin, FormView):
    form_class = forms.HelpOfferForm
    template_name = 'bikeanjo_help_offer.html'

    def get_success_url(self):
        return reverse('cyclist_register_routes')

    def get_form_kwargs(self):
        kwargs = super(HelpOfferView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user.cyclist
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(HelpOfferView, self).form_valid(form)


class HelpRequestView(LoginRequiredMixin, FormView):
    form_class = forms.HelpRequestForm
    template_name = 'requester_ask_help.html'

    def get_success_url(self):
        return reverse('cyclist_register_routes')

    def get_form_kwargs(self):
        kwargs = super(HelpRequestView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user.cyclist
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(HelpRequestView, self).form_valid(form)


class TrackRegisterView(LoginRequiredMixin, FormView):
    template_name = 'cyclist_routes_register_form.html'
    form_class = forms.TrackForm

    def get_success_url(self):
        return reverse('cyclist_registered_routes')

    def form_valid(self, form):
        form.save(cyclist=self.request.user.cyclist)
        return super(TrackRegisterView, self).form_valid(form)


class TrackListView(LoginRequiredMixin, FormView):
    template_name = 'cyclist_routes_list.html'
    form_class = forms.TrackReviewForm

    def get_success_url(self):
        return reverse('cyclist_register_points')

    def get_form_kwargs(self):
        kwargs = super(TrackListView, self).get_form_kwargs()
        kwargs['cyclist'] = self.request.user.cyclist
        return kwargs

    def form_valid(self, form):
        form.save(cyclist=self.request.user.cyclist)
        return super(TrackListView, self).form_valid(form)


class PointsRegisterView(LoginRequiredMixin, FormView):
    template_name = 'cyclist_free_points.html'
    form_class = forms.PointsForm

    def get_form_kwargs(self):
        kwargs = super(PointsRegisterView, self).get_form_kwargs()
        kwargs['cyclist'] = self.request.user.cyclist
        return kwargs

    def get_success_url(self):
        return reverse('cyclist_register_points')

    def form_valid(self, form):
        form.save()
        return super(PointsRegisterView, self).form_valid(form)


class HomeView(TemplateView):
    template_name = 'home.html'
