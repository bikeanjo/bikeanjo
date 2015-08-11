# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles import views
from django.views.generic import TemplateView

import front.views

admin.autodiscover()

urlpatterns = [
    # drf api
    url(r'^api/', include('cities.api_urls')),

    # the django admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rosetta/', include('rosetta.urls')),

    # django allauth
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/signup/$', TemplateView.as_view(template_name='signup_define_role.html'),
        name='signup_define_role'),
    url(r'^accounts/', include('allauth.urls')),

    # flatpages
    url(r'^pages/', include('django.contrib.flatpages.urls')),

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
    url(r'^requester/request-help/(?P<pk>\d+)/points/$',
        front.views.HelpRequestPointView.as_view(), name='requester_help_request_points'),
    url(r'^requester/request-help/(?P<pk>\d+)/message/$',
        front.views.HelpRequestMessageView.as_view(), name='requester_help_request_message'),

    url(r'^(?P<context>signup|dashboard)/register-routes-to-help/$',
        front.views.TrackRegisterView.as_view(), name='cyclist_register_routes'),
    url(r'^(?P<context>signup|dashboard)/registered-routes/$',
        front.views.TrackListView.as_view(), name='cyclist_registered_routes'),
    url(r'^(?P<context>signup|dashboard)/register-free-points/$',
        front.views.PointsRegisterView.as_view(), name='cyclist_register_points'),

    url(r'^signup/agreement/$',
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

    # Events
    url(r'^events/$',
        front.views.EventListView.as_view(), name='dashboard_event_list'),
    url(r'^events/(?P<slug>[\w-]+)/$',
        front.views.EventDetailView.as_view(), name='dashboard_event_detail'),

    # Events
    url(r'^dicas/$',
        front.views.TemplateView.as_view(template_name="about.html"), name='tips_list'),

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
    url(r'^contact/$',
        front.views.ContactView.as_view(), name='contact_view'),
    url(r'^newsletter/confirm/(?P<email>[^/]{6,254})/(?P<token>\w{64,64})/$',
        front.views.ConfirmSubscriptionView.as_view(), name='confirm_subscription_view'),

    url(r'^login/$', TemplateView.as_view(template_name="login.html")),
    url(r'^solicitante/$', TemplateView.as_view(template_name="dashboard_solicitante.html")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^tpl/(?P<tpl>.*)$',
            front.views.RawTemplateView.as_view(), name='raw_tpl_view'),
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
