# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0012_auto_20150514_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='helpreply',
            name='intention',
        ),
        migrations.RemoveField(
            model_name='helpreply',
            name='rating',
        ),
    ]
