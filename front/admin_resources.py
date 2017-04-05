# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from import_export import resources, fields
from front import models


class NewsletterResource(resources.ModelResource):
    class Meta:
        model = models.Subscriber
        fields = ('created_date', 'email', 'valid',)


class FeedbackResource(resources.ModelResource):
    created_date = fields.Field(column_name=_('Date of creation'))
    author_name = fields.Field(column_name=_('Name'))
    author_role = fields.Field(column_name=_('Role'))
    message = fields.Field(column_name=_('Message'))

    class Meta:
        model = models.Feedback
        fields = ('created_date', 'message',)
        export_order = ('created_date', 'author_name', 'author_role', 'message',)

    def dehydrate_created_date(self, obj):
        return obj.created_date.strftime('%d/%m/%Y')

    def dehydrate_author_name(self, obj):
        return obj.author.get_full_name()

    def dehydrate_author_role(self, obj):
        return _(obj.author.role.title())

    def dehydrate_message(self, obj):
        return obj.message


class HelpRequestResource(resources.ModelResource):
    created_date = fields.Field(column_name=_('Date of creation'))
    requester = fields.Field(column_name=_('Requester'))
    bikeanjo = fields.Field(column_name=_('Bikeanjo'))
    help_with = fields.Field(column_name=_('Help with'))
    status = fields.Field(column_name=_('Status'))
    rating = fields.Field(column_name=_('Rating'))

    class Meta:
        model = models.HelpRequest
        fields = ('created_date', 'requester', 'bikeanjo', 'help_with', 'status', 'rating',)
        export_order = ('created_date', 'requester', 'bikeanjo', 'help_with', 'status', 'rating',)

    def dehydrate_created_date(self, obj):
        return obj.created_date.strftime('%d/%m/%Y')

    def dehydrate_requester(self, obj):
        return obj.requester.get_full_name()

    def dehydrate_bikeanjo(self, obj):
        if obj and obj.bikeanjo:
            return obj.bikeanjo.get_full_name()
        return ''

    def dehydrate_help_with(self, obj):
        return obj.get_help_label()

    def dehydrate_status(self, obj):
        status_labels = models.HelpRequest.STATUS
        if obj.status:
            return status_labels.get(obj.status, '')
        return ''

    def dehydrate_rating(self, obj):
        if obj.requester_rating > 0:
            return obj.requester_rating
        return ''
