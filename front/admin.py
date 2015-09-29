from urllib import urlencode
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from front import models

import admin_resources as resources
import cyclists

admin.site.site_title = _('Bikeanjo')
admin.site.site_header = _('Bikeanjo administration')
admin.site.index_title = _('Site administration')


class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    list_filter = ('city', 'country', 'date_joined', 'last_login', 'accepted_agreement')
    resource_class = resources.UserResource

    def full_name(self, obj):
        return obj.get_full_name() or obj.username
    full_name.short_description = _('Full name')
    full_name.admin_order_field = 'first_name'

    def active_requests(self, obj):
        counter = 0
        if obj.role == 'bikeanjo':
            counter = obj.helpbikeanjo_set.active().count()
        elif obj.role == 'requester':
            counter = obj.helprequested_set.active().count()
        else:
            return '-'

        if counter > 0:
            query = {
                obj.role: obj.id,
                'status__in': 'new,open',
            }
            return format_html(
                '{} <small><a href="{}?{}">{}</a></small>',
                counter,
                reverse('admin:front_helprequest_changelist'),
                urlencode(query),
                _('List')
            )

        return counter
    active_requests.short_description = _('Active requests')

    def finalized_requests(self, obj):
        counter = 0
        if obj.role == 'bikeanjo':
            counter = obj.helpbikeanjo_set.filter(status='finalized').count()
        elif obj.role == 'requester':
            counter = obj.helprequested_set.filter(status='finalized').count()
        else:
            return '-'

        if counter > 0:
            query = {
                obj.role: obj.id,
                'status__in': 'finalized',
            }
            return format_html(
                '{} <small><a href="{}?{}">{}</a></small>',
                counter,
                reverse('admin:front_helprequest_changelist'),
                urlencode(query),
                _('List')
            )

        return counter
    finalized_requests.short_description = _('Finalized requests')

    def lookup_allowed(self, lookup, value):
        allow = [
            'contentreadlog__object_id',
            'contentreadlog__content_type__model',
            'contentreadlog__content_type__app_label',
        ]

        if lookup in allow:
            return True

        return super(CustomUserAdmin, self).lookup_allowed(lookup, value)


@admin.register(cyclists.models.User)
class User(CustomUserAdmin):
    list_display = ('full_name', 'email', 'role', 'date_joined',
                    'last_login', 'city', 'country', 'accepted_agreement')
    list_filter = ('role', 'city', 'country', 'date_joined', 'last_login', 'accepted_agreement')


@admin.register(cyclists.models.Requester)
class Requester(CustomUserAdmin):
    list_display = ('full_name', 'date_joined', 'last_login', 'city', 'country',
                    'active_requests', 'finalized_requests',)


@admin.register(cyclists.models.Bikeanjo)
class Bikeanjo(CustomUserAdmin):
    list_display = ('full_name', 'date_joined', 'last_login', 'available', 'city', 'country',
                    'active_requests', 'finalized_requests', 'service_rating',
                    'tracks', 'points')
    list_filter = ('city', 'country', 'available', 'date_joined', 'last_login')

    def service_rating(self, obj):
        if obj.role != 'bikeanjo':
            return '-'
        rating = obj.helpbikeanjo_set\
                    .filter(status='finalized')\
                    .aggregate(avg_rating=models.models.Avg('requester_rating'))\
                    .values()[0]
        return rating or 0
    service_rating.short_description = _('Service rating')

    def tracks(self, obj):
        counter = obj.track_set.count()
        if counter > 0:
            query = {'user': obj.id}
            return format_html(
                '{} <small><a href="{}?{}">{}</a></small>',
                counter,
                reverse('admin:front_track_changelist'),
                urlencode(query),
                _('List')
            )
        return counter
    tracks.short_description = _('Tracks')

    def points(self, obj):
        counter = obj.point_set.count()
        if counter > 0:
            query = {'user': obj.id}
            return format_html(
                '{} <small><a href="{}?{}">{}</a></small>',
                counter,
                reverse('admin:front_point_changelist'),
                urlencode(query),
                _('List')
            )
        return counter
    points.short_description = _('Points')


@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'user_name', 'start', 'end', 'track',)
    list_filter = ('created_date', 'user__role')
    search_fields = ('user__first_name', 'user__last_name', 'start', 'end')

    def user_name(self, obj):
        return format_html(
            u'<a href="{}">{}</a>',
            reverse('admin:cyclists_user_change', args=[obj.user.id]),
            obj.user.get_full_name()
        )
    user_name.admin_order_field = 'user__first_name'
    user_name.short_description = _('User name')


@admin.register(models.Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'address', 'coords',)
    list_filter = ('created_date', 'user__role')
    search_fields = ('user__first_name', 'user__last_name', 'address')

    def user_name(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:cyclists_user_change', args=[obj.user.id]),
            obj.user.get_full_name()
        )
    user_name.admin_order_field = 'user__first_name'
    user_name.short_description = _('User name')


class HelpReplyInline(admin.TabularInline):
    extra = 0
    model = models.HelpReply
    ordering = ['id']
    readonly_fields = ['created_date', 'author', 'message']


@admin.register(models.HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    inlines = [HelpReplyInline]
    search_fields = ('requester__first_name', 'requester__last_name',
                     'bikeanjo__first_name', 'bikeanjo__last_name',
                     'message',)
    list_display = ('created_date', 'requester_name', 'bikeanjo_name', 'get_help_label_',
                    'status', 'requester_rating', 'requester_eval',)
    list_filter = ('created_date', 'status', 'requester_rating',)

    def get_help_label_(self, obj):
        return obj.get_help_label()
    get_help_label_.short_description = _('Help with')
    get_help_label_.admin_order_field = 'help_with'

    def requester_name(self, obj):
        return obj.requester.get_full_name() or obj.requester.username
    requester_name.short_description = _('Requester name')

    def bikeanjo_name(self, obj):
        if obj.bikeanjo is None:
            return ''
        return obj.bikeanjo.get_full_name()
    bikeanjo_name.short_description = _('Bikeanjo name')
    bikeanjo_name.admin_order_field = 'bikeanjo__first_name'


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'title', 'readed_by_')
    list_filter = ('created_date',)
    search_fields = ('title',)

    def readed_by_(self, obj):
        return obj.readed_by.count()
    readed_by_.short_description = _('Readed by')


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'address',)
    list_filter = ('created_date', 'date',)
    search_fields = ('title', 'address', 'content')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'author_name', 'message',)
    list_filter = ('created_date',)
    search_fields = ('author__first_name', 'author__last_name', 'message',)

    def author_name(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:cyclists_user_change', args=[obj.author.id]),
            obj.author.get_full_name()
        )
    author_name.admin_order_field = 'author__first_name'
    author_name.short_description = _('Name')


@admin.register(models.Feedback)
class FeedbackAdmin(ImportExportModelAdmin):
    list_display = ('created_date', 'author_name', 'author_role', 'message',)
    list_filter = ('created_date', 'author__role',)
    search_fields = ('author__first_name', 'author__last_name', 'message')
    resource_class = resources.FeedbackResource

    def author_name(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:cyclists_user_change', args=[obj.author.id]),
            obj.author.get_full_name()
        )
    author_name.admin_order_field = 'author__first_name'
    author_name.short_description = _('Name')

    def author_role(self, obj):
        return _(obj.author.role.title())
    author_role.admin_order_field = 'author__role'
    author_role.short_description = _('Role')


@admin.register(models.Subscriber)
class SubscriberAdmin(ImportExportModelAdmin):
    list_display = ('created_date', 'email', 'token', 'valid',)
    list_filter = ('created_date', 'valid',)
    search_fields = ('email',)
    resource_class = resources.NewsletterResource


@admin.register(models.ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'email', 'subject', 'message',)
    list_filter = ('created_date', 'subject',)
    search_fields = ('message',)


@admin.register(models.TipForCycling)
class TipAdmin(admin.ModelAdmin):
    list_display = ('title', 'target', 'created_date',)
    list_filter = ('created_date', 'target',)
    search_fields = ('title', 'content',)
