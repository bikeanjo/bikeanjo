from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CyclistConfig(AppConfig):
    name = 'cyclists'
    verbose_name = _('Cyclists')
