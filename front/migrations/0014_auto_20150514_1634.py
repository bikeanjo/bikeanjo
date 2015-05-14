# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0013_auto_20150514_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='helprequest',
            name='requester_eval',
            field=models.TextField(verbose_name='message', blank=True),
        ),
        migrations.AddField(
            model_name='helprequest',
            name='requester_rating',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='rating'),
        ),
    ]
