# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0002_cyclist_point_track'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='end',
            field=models.CharField(default='start', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='track',
            name='start',
            field=models.CharField(default='end', max_length=64),
            preserve_default=False,
        ),
    ]
