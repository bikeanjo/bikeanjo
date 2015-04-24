from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from front import models


class UserCyclistInline(admin.StackedInline):
    model = models.Cyclist
    can_delete = False
    verbose_name_plural = 'Cyclists'
admin.site.unregister(User)


@admin.register(User)
class UserCyclistAdmin(UserAdmin):
    inlines = (UserCyclistInline, )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2'),
            'classes': ('wide',)
        }),
    )

    def save_formset(self, request, form, formset, change):
        cyclistForm = formset.forms[0]
        cyclistForm.instance = form.instance.cyclist

        super(UserCyclistAdmin, self).save_formset(request, form, formset, change)


@admin.register(models.Cyclist)
class CyclistAdmin(admin.ModelAdmin):
    list_display = ('the_full_name', 'the_email', 'country', 'city', 'gender',
                    'birthday', 'ride_experience', 'bike_use', 'the_help',
                    'role',)

    def the_full_name(self, obj):
        return '%s %s' % (
            obj.user.first_name,
            obj.user.last_name
        )

    def the_email(self, obj):
        return obj.user.email

    def the_help(self, obj):
        labels = '<br/>'.join([unicode(l)for l in obj.help_labels()])
        return mark_safe(labels)


@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('user', 'start', 'end', 'track',)
