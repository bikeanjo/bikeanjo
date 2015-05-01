# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='helprequest',
            name='last_access',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 30, 21, 26, 25, 247497, tzinfo=utc), verbose_name='access date', editable=False),
        ),
    ]
