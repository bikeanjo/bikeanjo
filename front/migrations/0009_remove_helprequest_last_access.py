# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0008_auto_20150505_1900'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='helprequest',
            name='last_access',
        ),
    ]
