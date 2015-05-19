# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q, Max
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView, DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.utils import timezone
from django.utils.http import is_safe_url, urlencode
from django.utils.translation import ugettext_lazy as _
import allauth.account.views
import forms
import models


class RegisteredUserMixin(LoginRequiredMixin):

    def get_agreement_url(self):
        url = reverse('cyclist_agreement')
        if REDIRECT_FIELD_NAME:
            url += '?' + urlencode({REDIRECT_FIELD_NAME: self.request.get_full_path()})
        return url

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and not request.user.accepted_agreement:
            return HttpResponseRedirect(self.get_agreement_url())
        return super(RegisteredUserMixin, self).dispatch(request, *args, **kwargs)


class RedirectUrlMixin(object):

    def get_redirect_url(self):
        field_name = self.get_redirect_field_name()
        next_page = self.request.session.pop(field_name, None)\
            or self.request.POST.get(field_name, None)\
            or self.request.GET.get(field_name, None)

        if next_page and is_safe_url(url=next_page, host=self.request.get_host()):
            return next_page

        return None


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('cyclist_dashboard'))
        return super(HomeView, self).get(request, **kwargs)


class RawTemplateView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        tpl = '%s.html' % self.kwargs.get('tpl')
        return [tpl]


#
# Views about user Profile on Dashboard
#
class DashboardMixin(RegisteredUserMixin):

    def get_context_data(self, **kwargs):
        data = super(DashboardMixin, self).get_context_data(**kwargs)
        data['unread'] = {
            'messages': models.Message.objects.exclude(readed_by__user=self.request.user),
            'events': models.Event.objects.exclude(readed_by__user=self.request.user),
        }
        return data


class DashBoardView(DashboardMixin, TemplateView):
    def get_template_names(self):
        tpl = '%s_dashboard.html' % self.request.user.role
        return [tpl]


class UserRegisterView(DashboardMixin, TemplateView):
    def get_template_names(self):
        tpl = '%s_dashboard_userregister.html' % self.request.user.role
        return [tpl]


class UserInfoUpdateView(DashboardMixin, UpdateView):
    template_name = 'cyclist_dashboard_userinfo.html'
    fields = ('first_name', 'last_name', 'email', 'country', 'city', 'gender', 'birthday',)

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('user_info_update')

    def form_valid(self, form):
        messages.success(self.request, _('Your information has been updated!'))
        return super(UserInfoUpdateView, self).form_valid(form)


class ExperienceUpdateView(DashboardMixin, UpdateView):
    form_class = forms.BikeanjoExperienceForm

    def get_template_names(self):
        tpl = '%s_dashboard_experience.html' % self.request.user.role
        return [tpl]

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('user_experience_update')


class PasswordResetView(DashboardMixin, UpdateView):
    template_name = 'cyclist_dashboard_changepassword.html'
    form_class = forms.PasswordResetForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('user_password_change')

    def form_valid(self, form):
        result = super(PasswordResetView, self).form_valid(form)
        update_session_auth_hash(self.request, form.instance)
        messages.success(self.request, 'Senha alterada!')
        return result
#
# Views about Dashboard
#


class RequestsListView(DashboardMixin, ListView):
    model = models.HelpRequest
    paginate_by = 10

    def get_template_names(self):
        if self.request.user.role == 'bikeanjo':
            return ['bikeanjo_dashboard_requests.html']
        return ['requester_dashboard_requests.html']

    def get_queryset(self):
        user = self.request.user
        qs = super(RequestsListView, self).get_queryset()
        qs = qs.filter(**{user.role: user})

        status = self.request.GET.get('status')
        if status in models.HelpRequest.STATUS:
            qs = qs.filter(status=status)

        return qs.annotate(last_reply=Max('helpreply__created_date'))


class NewRequestsListView(DashboardMixin, ListView):
    model = models.HelpRequest
    paginate_by = 10
    template_name = 'bikeanjo_dashboard_new_requests.html'

    def get_context_data(self, **kwargs):
        context = super(NewRequestsListView, self).get_context_data(**kwargs)
        context['no_new_requests'] = getattr(self, 'no_new_requests', False)

        context['filter'] = ''
        _filter = self.request.GET.get('filter')
        if _filter in ['orphan', 'new']:
            context['filter'] = _filter

        return context

    def get_queryset(self):
        '''
        Define queryset de acordo com filtro informado em POST.
        Se o filtro for new, mas não houver nenhum resultado, cria
        uma flag 'no_new_requests' nesta instância de View
        '''
        queryset = super(NewRequestsListView, self).get_queryset().filter(status='new')
        _filter = self.request.GET.get('filter')
        qs = queryset
        if _filter == 'new':
            qs = queryset.filter(bikeanjo=self.request.user)

            if qs.count() == 0:
                self.no_new_requests = True
                qs = queryset.filter(bikeanjo=None)

        elif _filter == 'orphan':
            qs = queryset.filter(bikeanjo=None)
        else:
            qs = queryset.filter(Q(bikeanjo=self.request.user) | Q(bikeanjo=None))
        return qs


class NewRequestDetailView(DashboardMixin, UpdateView):
    template_name = 'bikeanjo_dashboard_new_request.html'
    fields = ['status', ]
    model = models.HelpRequest

    def get_success_url(self):
        if self.object.status == 'open':
            return reverse('cyclist_request_detail', kwargs=self.kwargs)
        return reverse('cyclist_new_requests')

    def get_object(self):
        instance = super(NewRequestDetailView, self).get_object()
        instance.bikeanjo = self.request.user
        return instance


class RequestUpdateView(DashboardMixin, UpdateView):
    model = models.HelpRequest
    form_class = forms.HelpRequestUpdateForm

    def get(self, request, **kwargs):
        response = super(RequestUpdateView, self).get(request, **kwargs)

        if request.user.role in ['bikeanjo', 'requester']:
            field = '{0}_access'.format(request.user.role)
            self.model.objects.filter(id=self.object.id).update(**{field: timezone.now()})

        return response

    def get_success_url(self):
        return reverse('cyclist_request_detail', kwargs=self.kwargs)

    def get_template_names(self):
        if self.request.user.role == 'bikeanjo':
            return ['bikeanjo_dashboard_request.html']
        return ['requester_dashboard_request.html']


class RequestReplyFormView(RegisteredUserMixin, FormView):
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
        # messages.add_message(self.request, messages.SUCCESS, 'Sua resposta foi enviada com sucesso!')
        return super(RequestReplyFormView, self).form_valid(form)


class MessageListView(DashboardMixin, ListView):
    model = models.Message
    template_name = 'dashboard_message_list.html'

    def get_queryset(self):
        return models.Message.user_access_annotated(user=self.request.user)


class MessageDetailView(DashboardMixin, DetailView):
    model = models.Message
    template_name = 'dashboard_message_detail.html'

    def get(self, request, **kwargs):
        response = super(MessageDetailView, self).get(request, **kwargs)
        user = request.user
        if not self.object.readed_by.filter(user=user).exists():
            self.object.readed_by.create(user=user)
        return response


class EventListView(DashboardMixin, ListView):
    model = models.Event
    template_name = 'dashboard_event_list.html'

    def get_queryset(self):
        return models.Event.user_access_annotated(user=self.request.user)


class EventDetailView(DashboardMixin, DetailView):
    model = models.Event
    template_name = 'dashboard_event_detail.html'

    def get(self, request, **kwargs):
        response = super(EventDetailView, self).get(request, **kwargs)
        user = request.user
        if not self.object.readed_by.filter(user=user).exists():
            self.object.readed_by.create(user=user)
        return response

#
# Views to register user and his role
#


class SignupView(allauth.account.views.SignupView):

    def get(self, request, **kwargs):
        if 'role' not in self.kwargs:
            return HttpResponseRedirect(reverse('home'))
        request.session['user_role'] = self.kwargs.get('role')
        return super(SignupView, self).get(request, **kwargs)

    def get_success_url(self):
        if self.kwargs.get('role') == 'bikeanjo':
            return reverse('bikeanjo_account_signup_complete')
        return reverse('requester_account_signup_complete')

    def form_valid(self, form):
        response = super(SignupView, self).form_valid(form)
        self.request.user.role = self.kwargs.get('role')
        self.request.user.save()
        return response


class SignupBikeanjoView(LoginRequiredMixin, FormView):
    form_class = forms.SignupBikeanjoForm
    template_name = 'bikeanjo_complete_signup.html'

    def get_success_url(self):
        return reverse('bikeanjo_help_offer')

    def get_form_kwargs(self):
        kwargs = super(SignupBikeanjoView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(SignupBikeanjoView, self).form_valid(form)


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


class SignupAgreementView(LoginRequiredMixin, RedirectUrlMixin, UpdateView):
    form_class = forms.SignupAgreementForm
    model = models.User

    def get_template_names(self):
        tpl = '%s_signup_terms.html' % self.request.user.role
        return [tpl]

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.get_redirect_url() or\
            reverse('cyclist_dashboard')

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


class HelpRequestView(LoginRequiredMixin, RedirectUrlMixin, FormView):
    form_class = forms.HelpRequestForm
    template_name = 'requester_ask_help.html'

    def get_success_url(self):
        url = self.get_redirect_url()

        if url:
            return url
        if self.helprequest.help_with & 3 > 0:
            url = reverse('cyclist_register_points')
        elif self.helprequest.help_with & 12 > 0:
            url = reverse('requester_help_request_route',
                          args=[self.helprequest.id])

        return url or reverse('cyclist_request_detail')

    def get_form_kwargs(self):
        kwargs = super(HelpRequestView, self).get_form_kwargs()
        kwargs['requester'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.helprequest = form.save()
        return super(HelpRequestView, self).form_valid(form)


class HelpRequestRouteView(LoginRequiredMixin, RedirectUrlMixin, UpdateView):
    model = models.HelpRequest
    form_class = forms.HelpRequestRouteForm
    template_name = 'requester_ask_help_route.html'

    def get_success_url(self):
        return self.get_redirect_url() or\
            reverse('cyclist_request_detail', args=[self.object.id])


#
# Views to register tracks and places
#


class TrackRegisterView(LoginRequiredMixin, RedirectUrlMixin, FormView):
    template_name = 'cyclist_routes_register_form.html'
    form_class = forms.TrackForm

    def get_success_url(self):
        url = reverse('cyclist_registered_routes')
        redirect = self.get_redirect_url()

        if redirect:
            url = '%s?%s=%s' % (
                url,
                self.get_redirect_field_name(),
                redirect,
            )
        return url

    def get_form_kwargs(self):
        kwargs = super(TrackRegisterView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(TrackRegisterView, self).form_valid(form)


class TrackListView(LoginRequiredMixin, RedirectUrlMixin, FormView):
    template_name = 'cyclist_routes_list.html'
    form_class = forms.TrackReviewForm

    def get_success_url(self):
        return self.get_redirect_url() or\
            reverse('cyclist_register_points')

    def get_form_kwargs(self):
        kwargs = super(TrackListView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(TrackListView, self).form_valid(form)


class PointsRegisterView(LoginRequiredMixin, RedirectUrlMixin, FormView):
    template_name = 'cyclist_free_points.html'
    form_class = forms.PointsForm

    def get_form_kwargs(self):
        kwargs = super(PointsRegisterView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return self.get_redirect_url() or\
            reverse('cyclist_dashboard')

    def form_valid(self, form):
        form.save()
        return super(PointsRegisterView, self).form_valid(form)
