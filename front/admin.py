from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from front import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('role',)


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
    list_display = ('requester_name', 'volunteer_name', 'get_help_label',
                    'status', 'last_reply_date', 'requester_rating',
                    'requester_eval',)

    def requester_name(self, obj):
        return obj.requester.get_full_name()

    def volunteer_name(self, obj):
        if obj.volunteer is None:
            return ''
        return obj.volunteer.get_full_name()
