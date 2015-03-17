from django.apps import AppConfig


class FrontConfig(AppConfig):
    name = 'front'

    def ready(self):
        import signals
