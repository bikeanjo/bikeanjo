# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0007_auto_20150505_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='helprequest',
            name='requester_access',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='access date', editable=False),
        ),
        migrations.AddField(
            model_name='helprequest',
            name='volunteer_access',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='access date', editable=False),
        ),
    ]
