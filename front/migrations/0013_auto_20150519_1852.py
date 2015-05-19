# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0012_auto_20150519_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='reason',
            field=models.CharField(max_length=128, blank=True),
        ),
    ]
