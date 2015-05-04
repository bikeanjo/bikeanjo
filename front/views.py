# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView, DetailView
from django.views.generic.list import ListView

import allauth.account.views
import forms
import models


class HomeView(TemplateView):
    template_name = 'home.html'

#
# Views for Dashboard
#


class DashBoardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.role == 'volunteer':
            return ['requester_dashboard.html']
        return ['requester_dashboard.html']


class RequestsListView(LoginRequiredMixin, ListView):
    template_name = 'requester_dashboard_requests.html'
    model = models.HelpRequest
    paginate_by = 10

    def get_queryset(self):
        qs = super(RequestsListView, self).get_queryset()
        qs = qs.filter(requester=self.request.user)

        status = self.request.GET.get('status')
        if status in models.HelpRequest.STATUS:
            qs = qs.filter(status=status)

        return qs


class RequestDetailView(LoginRequiredMixin, DetailView):
    template_name = 'requester_dashboard_request.html'
    model = models.HelpRequest


class RequestReplyFormView(LoginRequiredMixin, FormView):
    form_class = forms.RequestReplyForm

    def get(self, request, **kwargs):
        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def get_success_url(self):
        return reverse('cyclist_request_detail', kwargs=self.kwargs)

    def get_form_kwargs(self):
        kwargs = super(RequestReplyFormView, self).get_form_kwargs()
        kwargs['author'] = self.request.user
        kwargs['helprequest'] = get_object_or_404(models.HelpRequest, **self.kwargs)
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(RequestReplyFormView, self).form_valid(form)
#
# Views to register user and his role
#


class SignupView(allauth.account.views.SignupView):
    def get(self, request, **kwargs):
        request.session['user_role'] = self.kwargs.get('role')
        return super(SignupView, self).get(request, **kwargs)

    def get_success_url(self):
        if self.kwargs.get('role') == 'volunteer':
            return reverse('volunteer_account_signup_complete')
        return reverse('requester_account_signup_complete')

    def form_valid(self, form):
        response = super(SignupView, self).form_valid(form)
        self.request.user.role = self.kwargs.get('role')
        self.request.user.save()
        return response


class SignupVolunteerView(LoginRequiredMixin, FormView):
    form_class = forms.SignupVolunteerForm
    template_name = 'bikeanjo_complete_signup.html'

    def get_success_url(self):
        return reverse('volunteer_help_offer')

    def get_form_kwargs(self):
        kwargs = super(SignupVolunteerView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
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
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(SignupRequesterView, self).form_valid(form)


#
# Views to get cyclist info
#


class HelpOfferView(LoginRequiredMixin, FormView):
    form_class = forms.HelpOfferForm
    template_name = 'bikeanjo_help_offer.html'

    def get_success_url(self):
        return reverse('cyclist_register_routes')

    def get_form_kwargs(self):
        kwargs = super(HelpOfferView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
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
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(HelpRequestView, self).form_valid(form)


#
# Views to register tracks and places
#


class TrackRegisterView(LoginRequiredMixin, FormView):
    template_name = 'cyclist_routes_register_form.html'
    form_class = forms.TrackForm

    def get_success_url(self):
        if self.request.user.role == 'volunteer':
            return reverse('cyclist_registered_routes')
        return reverse('cyclist_register_points')

    def get_form_kwargs(self):
        kwargs = super(TrackRegisterView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(TrackRegisterView, self).form_valid(form)


class TrackListView(LoginRequiredMixin, FormView):
    template_name = 'cyclist_routes_list.html'
    form_class = forms.TrackReviewForm

    def get_success_url(self):
        return reverse('cyclist_register_points')

    def get_form_kwargs(self):
        kwargs = super(TrackListView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(TrackListView, self).form_valid(form)


class PointsRegisterView(LoginRequiredMixin, FormView):
    template_name = 'cyclist_free_points.html'
    form_class = forms.PointsForm

    def get_form_kwargs(self):
        kwargs = super(PointsRegisterView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('cyclist_dashboard')

    def form_valid(self, form):
        form.save()
        return super(PointsRegisterView, self).form_valid(form)
