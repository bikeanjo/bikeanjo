# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0012_auto_20150424_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='point',
            name='cyclist',
        ),
        migrations.RemoveField(
            model_name='track',
            name='cyclist',
        ),
    ]
