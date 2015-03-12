from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from front.models import Cyclist


class CyclistInline(admin.StackedInline):
    model = Cyclist
    can_delete = False
    verbose_name_plural = 'Cyclist'


class UserAdmin(UserAdmin):
    inlines = (CyclistInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
