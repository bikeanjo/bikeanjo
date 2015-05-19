# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static

import front.views

admin.autodiscover()

urlpatterns = [
    # the django admin
    url(r'^admin/', include(admin.site.urls)),

    # django allauth
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/signup/$', front.views.SignupView.as_view()),
    url(r'^accounts/', include('allauth.urls')),

    # bikeanjo urls
    url(r'^$', front.views.HomeView.as_view(), name='home'),

    url(r'^(?P<role>bikeanjo|requester)/signup/$',
        front.views.SignupView.as_view(), name='cyclist_account_signup'),

    url(r'^bikeanjo/signup/complete/$',
        front.views.SignupBikeanjoView.as_view(), name='bikeanjo_account_signup_complete'),
    url(r'^requester/signup/complete/$',
        front.views.SignupRequesterView.as_view(), name='requester_account_signup_complete'),

    url(r'^bikeanjo/offer-help/$',
        front.views.HelpOfferView.as_view(), name='bikeanjo_help_offer'),

    url(r'^requester/request-help/$',
        front.views.HelpRequestView.as_view(), name='requester_help_request'),
    url(r'^requester/request-help/(?P<pk>\d+)/route/$',
        front.views.HelpRequestRouteView.as_view(), name='requester_help_request_route'),

    url(r'^cyclist/register-routes-to-help/$',
        front.views.TrackRegisterView.as_view(), name='cyclist_register_routes'),
    url(r'^cyclist/registered-routes/$',
        front.views.TrackListView.as_view(), name='cyclist_registered_routes'),
    url(r'^cyclist/register-free-points/$',
        front.views.PointsRegisterView.as_view(), name='cyclist_register_points'),

    url(r'^cyclist/signup/agreement/$',
        front.views.SignupAgreementView.as_view(), name='cyclist_agreement'),

    #
    # Dashboard HelpRequest and HelpReply
    #
    url(r'^dashboard/$',
        front.views.DashBoardView.as_view(), name='cyclist_dashboard'),

    url(r'^dashboard/my-requests/$',
        front.views.RequestsListView.as_view(), name='cyclist_my_requests'),
    url(r'^dashboard/new-requests/$',
        front.views.NewRequestsListView.as_view(), name='cyclist_new_requests'),
    url(r'^dashboard/new-request/(?P<pk>[1-9]\d*)/$',
        front.views.NewRequestDetailView.as_view(), name='cyclist_new_request_detail'),
    url(r'^dashboard/request/(?P<pk>[1-9]\d*)/$',
        front.views.RequestUpdateView.as_view(), name='cyclist_request_detail'),
    url(r'^dashboard/request/(?P<pk>[1-9]\d*)/reply/$',
        front.views.RequestReplyFormView.as_view(), name='cyclist_request_reply'),
    url(r'^dashboard/messages/$',
        front.views.MessageListView.as_view(), name='dashboard_message_list'),
    url(r'^dashboard/messages/(?P<pk>[1-9]\d*)/$',
        front.views.MessageDetailView.as_view(), name='dashboard_message_detail'),
    url(r'^dashboard/events/$',
        front.views.EventListView.as_view(), name='dashboard_event_list'),
    url(r'^dashboard/events/(?P<pk>[1-9]\d*)/$',
        front.views.EventDetailView.as_view(), name='dashboard_event_detail'),

    #
    # Dashboard User Info and Profile
    #
    url(r'^dashboard/register/$',
        front.views.UserRegisterView.as_view(), name='user_register'),
    url(r'^dashboard/register/user/$',
        front.views.UserInfoUpdateView.as_view(), name='user_info_update'),
    url(r'^dashboard/register/experience/$',
        front.views.ExperienceUpdateView.as_view(), name='user_experience_update'),
    url(r'^dashboard/register/change-password/',
        front.views.PasswordResetView.as_view(), name='user_password_change'),

    url(r'^feedback/$',
        front.views.FeedbackView.as_view(), name='user_feedback'),

    url(r'^login/$', TemplateView.as_view(template_name="login.html")),
    url(r'^solicitante/$', TemplateView.as_view(template_name="dashboard_solicitante.html")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^tpl/(?P<tpl>.*)$',
            front.views.RawTemplateView.as_view(), name='raw_tpl_view'),
    ]
