# -*- coding: utf-8 -*-

import os
import re
from django.conf import settings
from django.db import models, migrations


def load_flatpages_from_template(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0024_auto_20150706_2159'),
    ]

    operations = [
        migrations.RunPython(load_flatpages_from_template)
    ]
