# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.contrib.flatpages.models import FlatPage

from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TranslationAdmin
from dal import autocomplete

from front import models

import admin_resources as resources

admin.site.site_title = _('Bike Anjo')
admin.site.site_header = _('Bike Anjo Admin')
admin.site.index_title = _('Site Admin')


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
            u'<a href="{}">{}</a>',
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
    requester_name.short_description = _('New cyclist name')

    def bikeanjo_name(self, obj):
        if obj.bikeanjo is None:
            return ''
        return obj.bikeanjo.get_full_name()
    bikeanjo_name.short_description = _('Bike anjo name')
    bikeanjo_name.admin_order_field = 'bikeanjo__first_name'


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
        )

    list_display = ('created_date', 'title', 'readed_by_')
    list_filter = ('created_date',)
    search_fields = ('title',)

    def readed_by_(self, obj):
        return obj.readed_by.count()
    readed_by_.short_description = _('Read by')

    def get_form(self, *argz, **kwargz):
        form = super(MessageAdmin, self).get_form(*argz, **kwargz)
        form.base_fields['target_country'].widget = autocomplete.ModelSelect2(url='ac_country')
        form.base_fields['target_city'].widget = autocomplete.ModelSelect2(url='ac_city')
        return form


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
            u'<a href="{}">{}</a>',
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
            u'<a href="{}">{}</a>',
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


class TranslationAdminMedia(TranslationAdmin):
    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(models.Event)
class EventAdmin(TranslationAdminMedia):
    list_display = ('title', 'date', 'address',)
    list_filter = ('created_date', 'date',)
    search_fields = ('title', 'address', 'content')
    prepopulated_fields = {"slug": ("title",)}

    def get_form(self, *argz, **kwargz):
        form = super(EventAdmin, self).get_form(*argz, **kwargz)
        form.base_fields['city'].widget = autocomplete.ModelSelect2(url='ac_city')
        return form


admin.site.unregister(FlatPage)


@admin.register(FlatPage)
class FlatPageAdmin(TranslationAdminMedia):
    list_display = ('url', 'title')
    list_filter = ('sites', 'enable_comments', 'registration_required')
    search_fields = ('url', 'title')


@admin.register(models.TipForCycling)
class TipAdmin(TranslationAdminMedia):
    list_display = ('title', 'target', 'created_date',)
    list_filter = ('created_date', 'target',)
    search_fields = ('title', 'content',)
