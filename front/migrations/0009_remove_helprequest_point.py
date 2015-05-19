# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0008_auto_20150519_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='helprequest',
            name='point',
        ),
    ]
