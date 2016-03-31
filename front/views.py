# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.models import Site
from django.db.models import Q, Max
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView, DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.utils import timezone
from django.utils.http import is_safe_url, urlencode
from django.utils.translation import ugettext_lazy as _

from datastructures import Join
from django.db.models.sql.constants import LOUTER

import allauth.account.views
import forms
import models

import cyclists.models
from notifications import notify_admins_about_new_contact_message, notify_user_subscribed_in_newsletter


class RegisteredUserMixin(LoginRequiredMixin):

    def get_agreement_url(self):
        role = self.request.user.role
        url = reverse('cyclist_account_resignup', args=[role])
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


class HomeView(CreateView):
    template_name = 'home.html'
    model = models.Subscriber
    fields = ['email']

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['testimonies'] = models.Testimony.objects.select_related('author').reverse()[:5]
        context['counters'] = {
            'bikeanjos': cyclists.models.Bikeanjo.objects.count(),
            'requests': models.HelpRequest.objects.count(),
            'cities': cyclists.models.Bikeanjo.objects.order_by('city').distinct('city').count(),
            'countries': cyclists.models.Bikeanjo.objects.order_by('country').distinct('country').count(),
        }
        context['force_header'] = True
        context['force_footer'] = True
        context['site'] = Site.objects.filter(id=settings.SITE_ID).first()
        return context

    def get(self, request, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('cyclist_dashboard'))
        return super(HomeView, self).get(request, **kwargs)

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        response = super(HomeView, self).form_valid(form)
        notify_user_subscribed_in_newsletter(form.instance)
        return response


class RawTemplateView(TemplateView):
    def get_template_names(self):
        tpl = '%s.html' % self.kwargs.get('tpl')
        return [tpl]


#
# Views about user Profile on Dashboard
#
class DashboardMixin(RegisteredUserMixin):

    def get_context_data(self, **kwargs):
        user = self.request.user
        data = super(DashboardMixin, self).get_context_data(**kwargs)
        data['unread'] = {
            'messages': models.Message.objects.exclude(readed_by__user=user) .filter(created_date__gt=user.date_joined),
        }

        if user.role == 'bikeanjo':
            data['unread']['requests'] = user.helpbikeanjo_set.unread()
        elif user.role == 'requester':
            data['unread']['requests'] = user.helprequested_set.unread()

        data['unread']['total'] = sum((qs.count() for qs in data['unread'].values()))
        data['site'] = Site.objects.filter(id=settings.SITE_ID).first()
        data['force_header'] = True
        return data


class DashBoardView(DashboardMixin, TemplateView):

    def get_context_data(self, **kwargs):
        data = super(DashBoardView, self).get_context_data(**kwargs)
        data['first_access'] = self.request.session.pop('first_access', False)
        data['tip'] = self.get_tip()
        data['helprequest_list'] = self.get_helprequest_list()
        data['event_list'] = self.get_event_list()
        return data

    def get_tip(self):
        return models.TipForCycling.objects\
                     .filter(target__in=[self.request.user.role, 'all'])\
                     .order_by('?').first()

    def get_helprequest_list(self):
        return models.HelpRequest.objects.open()\
                     .filter(**{self.request.user.role: self.request.user})\
                     .annotate(last_reply=Max('helpreply__created_date'))

    def get_event_list(self):
        user = self.request.user

        event_list = models.Event.objects.filter(city=user.v1_city, date__gte=timezone.now())
        setattr(event_list, 'near', True)

        if not event_list.exists():
            event_list = models.Event.objects.filter(date__gt=timezone.now())
            setattr(event_list, 'near', False)

        return event_list.order_by('date')

    def get_template_names(self):
        role = self.request.user.role or 'requester'
        tpl = '%s_dashboard.html' % role
        return [tpl]


class UserRegisterView(DashboardMixin, TemplateView):
    template_name = 'cyclist_dashboard_userregister.html'


class UserInfoUpdateView(DashboardMixin, UpdateView):
    fields = ('first_name', 'last_name', 'email', 'country', 'city', 'gender', 'birthday',)

    def get_template_names(self):
        role = self.request.user.role or 'requester'
        tpl = '%s_dashboard_userinfo.html' % role
        return [tpl]

    def get_form_class(self):
        if self.request.user.role == 'bikeanjo':
            return forms.BikeanjoUserInforForm
        return forms.RequesterUserInforForm

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
        qs = qs.filter(requester__accepted_agreement=True)

        status = self.request.GET.get('status')
        if status in models.HelpRequest.STATUS:
            qs = qs.filter(status=status)

        qs = qs.order_by('-id')
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
        user = self.request.user
        queryset = super(NewRequestsListView, self).get_queryset().filter(status='new').exclude(requester=user)
        _filter = self.request.GET.get('filter')
        qs = queryset

        if _filter == 'new':
            qs = queryset.filter(bikeanjo=user)

            if qs.count() == 0:
                self.no_new_requests = True
                qs = queryset.filter(bikeanjo=None, requester__city=user.city)

        elif _filter == 'orphan':
            qs = queryset.filter(bikeanjo=None, requester__city=user.city)
        else:
            qs = queryset.filter(Q(bikeanjo=user) | Q(bikeanjo=None))

        qs = qs.order_by('-id')
        qs = qs.filter(requester__accepted_agreement=True)
        return qs


class NewRequestDetailView(DashboardMixin, UpdateView):
    template_name = 'bikeanjo_dashboard_new_request.html'
    form_class = forms.BikeanjoAcceptRequestForm
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

    def get_form_kwargs(self):
        kwargs = super(RequestUpdateView, self).get_form_kwargs()
        kwargs['data'] = kwargs.get('data').dict() if 'data' in kwargs else {}
        kwargs['data']['closed_by'] = self.request.user.role
        return kwargs

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
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        qs = models.Message.objects\
                   .filter(id__gt=0, created_date__gt=user.date_joined)\
                   .extra(select={'was_read': 'front_readedmessage.user_id'})
        join = Join(
            models.ReadedMessage._meta.db_table,
            models.Message._meta.db_table,
            None, LOUTER,
            models.Message.readed_by.related,
            True
        )
        join.add_field_val_restriction(
            models.ReadedMessage.user.field,
            user.id
        )
        qs.query.join(join)
        qs = qs.order_by('-id')
        return qs


class MessageDetailView(DashboardMixin, DetailView):
    model = models.Message
    template_name = 'dashboard_message_detail.html'

    def get(self, request, **kwargs):
        response = super(MessageDetailView, self).get(request, **kwargs)
        user = request.user
        if not self.object.readed_by.filter(user=user).exists():
            self.object.readed_by.create(user=user)
        return response


class EventListView(ListView):
    model = models.Event
    template_name = 'event_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        context['categories'] = models.Category.objects.all()
        context['cities'] = models.Event.objects\
                                        .order_by('city')\
                                        .distinct('city')\
                                        .values_list('city', flat=True)
        return context

    def get_queryset(self):
        qs = super(EventListView, self).get_queryset().filter(date__gte=timezone.now())

        filters = {}
        for f in self.request.GET.keys():
            if f in ['category', 'city']:
                filters[f] = self.request.GET.get(f, '')

        qs = qs.filter(**filters).order_by('-id')
        return qs


class EventDetailView(DetailView):
    model = models.Event
    template_name = 'event_detail.html'

    def get_context_data(self, **kwargs):
        data = super(EventDetailView, self).get_context_data(**kwargs)
        data['site'] = Site.objects.filter(id=settings.SITE_ID).first()
        if data['site']:
            for app in data['site'].socialapp_set.all():
                data[app.provider] = app
        return data

#
# Views to register user and his role
#


class SignupView(allauth.account.views.SignupView):

    def get(self, request, **kwargs):
        if 'role' not in self.kwargs:
            return HttpResponseRedirect(reverse('signup_define_role'))
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


class ReSignupView(LoginRequiredMixin, UpdateView):
    form_class = forms.SignupForm
    model = models.User
    template_name = 'account/signup.html'

    def get_object(self):
        return get_object_or_404(self.model, **{'id': self.request.user.id})

    def get_success_url(self):
        if self.kwargs.get('role') == 'bikeanjo':
            return reverse('bikeanjo_account_signup_complete')
        return reverse('requester_account_signup_complete')

    def form_valid(self, form):
        response = super(ReSignupView, self).form_valid(form)
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

    def has_steps_ok(self):
        session = self.request.session
        return 'helprequest_01' in session and 'helprequest_02' in session

    def cancel_steps(self):
        session = self.request.session
        if 'helprequest_01' in session:
            del session['helprequest_01']
        if 'helprequest_02' in session:
            del session['helprequest_02']

    def helprequest_form_part(self):
        if not self.has_steps_ok():
            return

        data = dict()
        data['message'] = self.request.POST.dict().get('message', '')
        data['help_with'] = self.request.session.get('helprequest_01')['help_with']
        data['geo_json'] = self.request.session.get('helprequest_02')
        form = forms.HelpRequestCompleteForm(data)
        return form

    def get_template_names(self):
        role = self.request.user.role or 'requester'
        tpl = '%s_signup_terms.html' % role
        return [tpl]

    def get(self, request, **kwargs):
        if not self.has_steps_ok():
            self.cancel_steps()
        return super(SignupAgreementView, self).get(request, *kwargs)

    def get_form_kwargs(self):
        kwargs = super(SignupAgreementView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        form2 = self.helprequest_form_part()

        response = None
        if form.is_valid():
            response = self.form_valid(form)
            if form2 and form2.is_valid():
                form2.instance.requester = form.instance
                form2.save()
                self.cancel_steps()
        else:
            response = self.form_invalid(form)
        return response

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        self.request.session['first_access'] = True
        return self.get_redirect_url() or\
            reverse('cyclist_dashboard')

#
# Views to get cyclist info
#


class HelpOfferView(LoginRequiredMixin, FormView):
    form_class = forms.HelpOfferForm
    template_name = 'bikeanjo_help_offer.html'

    def get_success_url(self):
        return reverse('cyclist_register_routes', args=['signup'])

    def get_form_kwargs(self):
        kwargs = super(HelpOfferView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(HelpOfferView, self).form_valid(form)


# Part 1 - Escolher tipo de ajuda
class HelpRequestView(LoginRequiredMixin, RedirectUrlMixin, FormView):
    form_class = forms.HelpRequestForm
    template_name = 'requester_ask_help.html'

    def get_success_url(self):
        url = self.get_redirect_url()

        if url:
            return url
        if self.helprequest.help_with & 3 > 0:
            url = reverse('requester_help_request_points')
        elif self.helprequest.help_with & 12 > 0:
            url = reverse('requester_help_request_route')

        return url or reverse('cyclist_request_detail')

    def get_form_kwargs(self):
        kwargs = super(HelpRequestView, self).get_form_kwargs()
        kwargs['requester'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.helprequest = form.instance
        self.request.session['helprequest_01'] = form.cleaned_data
        return super(HelpRequestView, self).form_valid(form)


# Step 2 - Escolher um lugar
class HelpRequestRouteView(LoginRequiredMixin, RedirectUrlMixin, FormView):
    form_class = forms.HelpRequestRouteForm
    template_name = 'requester_ask_help_route.html'

    def get_success_url(self):
        return self.get_redirect_url() or\
            reverse('requester_help_request_message')

    def form_valid(self, form):
        self.request.session['helprequest_02'] = form.cleaned_data
        return super(HelpRequestRouteView, self).form_valid(form)


# Step 2 - Escolher um lugar
class HelpRequestPointView(LoginRequiredMixin, RedirectUrlMixin, FormView):
    form_class = forms.HelpRequestPointForm
    template_name = 'requester_ask_help_points.html'

    def get_success_url(self):
        return self.get_redirect_url() or\
            reverse('requester_help_request_message')

    def form_valid(self, form):
        self.request.session['helprequest_02'] = form.cleaned_data
        return super(HelpRequestPointView, self).form_valid(form)


# Step 3 - Recebe descrição do usuario e grava pedido
class HelpRequestMessageView(LoginRequiredMixin, RedirectUrlMixin, CreateView):
    model = models.HelpRequest
    form_class = forms.HelpRequestCompleteForm
    template_name = 'requester_ask_help_message.html'

    def has_steps_ok(self):
        session = self.request.session
        return 'helprequest_01' in session and 'helprequest_02' in session

    def cancel_steps(self):
        session = self.request.session
        if 'helprequest_01' in session:
            del session['helprequest_01']
        if 'helprequest_02' in session:
            del session['helprequest_02']

    def get(self, request, **kwargs):
        if self.has_steps_ok():
            return super(HelpRequestMessageView, self).get(request, *kwargs)
        self.cancel_steps()
        return HttpResponseRedirect(reverse('requester_help_request'))

    def post(self, request, **kwargs):
        if self.has_steps_ok():
            return super(HelpRequestMessageView, self).post(request, *kwargs)
        self.cancel_steps()
        return HttpResponseRedirect(reverse('requester_help_request'))

    def get_form_kwargs(self):
        data = {}
        data['help_with'] = self.request.session['helprequest_01']['help_with']
        data['geo_json'] = self.request.session['helprequest_02']
        data.update(self.request.POST.dict())

        kwargs = super(HelpRequestMessageView, self).get_form_kwargs()
        kwargs['data'] = data
        return kwargs

    def form_valid(self, form):
        self.cancel_steps()
        form.instance.requester = self.request.user
        return super(HelpRequestMessageView, self).form_valid(form)

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
        url = reverse('cyclist_registered_routes',
                      args=[self.kwargs.get('context')])
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
            reverse('cyclist_register_points',
                    args=[self.kwargs.get('context')])

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


class FeedbackView(LoginRequiredMixin, RedirectUrlMixin, FormView):
    form_class = forms.FeedbackForm

    def get(self, request, **kwargs):
        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def get_success_url(self):
        return self.get_redirect_url() or\
            reverse('cyclist_dashboard')

    def get_form_kwargs(self):
        kwargs = super(FeedbackView, self).get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Seu feedback foi enviado. Obrigado!')
        return super(FeedbackView, self).form_valid(form)


class ConfirmSubscriptionView(DetailView):
    template_name = 'subscription_confirmed.html'
    model = models.Subscriber

    def get_context_data(self, **kwargs):
        context = super(ConfirmSubscriptionView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        response = super(ConfirmSubscriptionView, self).get(request, **kwargs)
        self.model.objects.filter(id=self.object.id).update(valid=True)
        return response

    def get_object(self):
        return get_object_or_404(self.model, **self.kwargs)


class ContactView(CreateView):
    fields = ('name', 'email', 'subject', 'message',)
    model = models.ContactMessage
    template_name = 'contact_form.html'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['force_header'] = True
        context['force_footer'] = True
        return context

    def form_valid(self, form):
        [message for message in messages.get_messages(self.request)]
        form.save()
        notify_admins_about_new_contact_message(form.instance)
        messages.success(self.request, 'Sua mensagem foi enviada!')
        return super(ContactView, self).form_valid(form)

    def get_success_url(self):
        return reverse('contact_view')


class TipsListView(ListView):
    model = models.TipForCycling
    template_name = 'tips.html'
    paginate_by = 10

    def get_queryset(self):
        target = self.kwargs.get('target')
        if target:
            return models.TipForCycling.objects.filter(target__in=[target, 'all'])
        return models.TipForCycling.objects.filter(target='all')


class BecomeBikeanjo(DashboardMixin, UpdateView):
    model = cyclists.models.User
    fields = ('role', 'accepted_agreement')

    def get(self, request, **kwargs):
        return HttpResponseNotAllowed('METHOD NOT ALLOWED')

    def get_form_kwargs(self):
        return {
            'instance': self.request.user,
            'data': {'role': 'bikeanjo', 'accepted_agreement': False}
        }

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('bikeanjo_account_signup_complete')
