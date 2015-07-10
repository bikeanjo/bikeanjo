from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FrontConfig(AppConfig):
    name = 'front'
    verbose_name = _('Control Panel')

    def ready(self):
        import signals
