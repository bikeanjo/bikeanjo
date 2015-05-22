from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from front import models

admin.site.site_title = _('Bikeanjo')
admin.site.site_header = _('Bikeanjo administration')
admin.site.index_title = _('Site administration')


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = ('full_name', 'is_active', 'city', 'role', 'active_requests',
                    'finalized_requests', 'service_rating')

    def full_name(self, obj):
        return obj.get_full_name() or obj.username

    def active_requests(self, obj):
        counter = '-'
        if obj.role == 'bikeanjo':
            counter = obj.helpbikeanjo_set.active().count()
        elif obj.role == 'requester':
            counter = obj.helprequested_set.active().count()
        return counter
    active_requests.short_description = _('Active requests')

    def finalized_requests(self, obj):
        counter = '-'
        if obj.role == 'bikeanjo':
            counter = obj.helpbikeanjo_set.filter(status='finalized').count()
        elif obj.role == 'requester':
            counter = obj.helprequested_set.filter(status='finalized').count()
        return counter
    finalized_requests.short_description = _('Finalized requests')

    def service_rating(self, obj):
        if obj.role != 'bikeanjo':
            return '-'
        rating = obj.helpbikeanjo_set\
                    .filter(status='finalized')\
                    .aggregate(avg_rating=models.models.Avg('requester_rating'))\
                    .values()[0]
        return rating or 0
    service_rating.short_description = _('Service rating')


@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('user', 'start', 'end', 'track',)


class HelpReplyInline(admin.TabularInline):
    extra = 0
    model = models.HelpReply
    ordering = ['id']
    readonly_fields = ['created_date', 'author', 'message']


@admin.register(models.HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    inlines = [HelpReplyInline]
    list_display = ('requester_name', 'bikeanjo_name', 'get_help_label',
                    'status', 'requester_rating', 'requester_eval',)

    def requester_name(self, obj):
        return obj.requester.get_full_name()

    def bikeanjo_name(self, obj):
        if obj.bikeanjo is None:
            return ''
        return obj.bikeanjo.get_full_name()


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'readed_by_')
    search_fields = ('title',)

    def readed_by_(self, obj):
        return obj.readed_by.count()
    readed_by_.short_description = _('Readed by')


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'address',)
