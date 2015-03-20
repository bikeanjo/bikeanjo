from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from front.models import Cyclist


class CyclistInline(admin.StackedInline):
    model = Cyclist
    can_delete = False
    verbose_name_plural = 'Cyclists'


class CyclistAdmin(UserAdmin):
    inlines = (CyclistInline, )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2'),
            'classes': ('wide',)
        }),
    )

    def save_formset(self, request, form, formset, change):
        cyclistForm = formset.forms[0]
        cyclistForm.instance = form.instance.cyclist

        super(CyclistAdmin, self).save_formset(request, form, formset, change)


admin.site.unregister(User)
admin.site.register(User, CyclistAdmin)
