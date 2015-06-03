# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0007_auto_20150603_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 6, 3, 0, 7, 51, 306238), verbose_name='Date'),
            preserve_default=False,
        ),
    ]
