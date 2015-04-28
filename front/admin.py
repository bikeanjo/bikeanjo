from django.contrib import admin
from front import models

@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('user', 'start', 'end', 'track',)
