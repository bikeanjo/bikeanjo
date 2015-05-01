# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0002_helprequest_last_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helprequest',
            name='last_access',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='access date', editable=False),
        ),
    ]
