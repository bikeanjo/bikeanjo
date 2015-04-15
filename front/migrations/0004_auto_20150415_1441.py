# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0003_auto_20150414_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='end',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='track',
            name='start',
            field=models.CharField(max_length=128),
        ),
    ]
