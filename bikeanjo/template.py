from pathlib import Path
import io
from os.path import dirname, join, abspath
from django.db import models
from django.apps import apps
from django.template import TemplateDoesNotExist
from django.template.loaders.base import Loader as BaseLoader

class Loader(BaseLoader):
    is_usable = True

    def get_template_path(self, app_template_name, template_dirs=None):
        print('>>>>>>>>>>>>>>' + app_template_name)
        template_parts = app_template_name.split(":", 1)

        if len(template_parts) != 2:
            app_name, template_name = "front", template_parts[0]
            # raise TemplateDoesNotExist()
        else:
            app_name, template_name = template_parts
            
        app_dir = apps.get_app_config(app_name).path
        template_dir = Path(app_dir) / 'templates'

        return str(template_dir / template_name)

    def load_template_source(self, template_name, template_dirs=None):

        filepath = self.get_template_path(template_name, template_dirs)
        try:
            with io.open(filepath, encoding=self.engine.file_charset) as fp:
                return fp.read(), filepath
        except IOError:
            pass
        raise TemplateDoesNotExist(template_name)
