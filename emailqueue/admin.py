from django.contrib import admin
from emailqueue.models import QueuedMail


@admin.register(QueuedMail)
class QueuedMailAdmin(admin.ModelAdmin):
    list_filter = ('date', 'tag', 'sent',)
    list_display = ('to', 'sender', 'date', 'tag', 'sent', 'subject', 'errors',)
    search_fields = ('local', 'relato', 'agente', 'projeto', 'linha_estrategica')