# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0011_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='score',
            field=models.FloatField(default=0),
        ),
    ]
