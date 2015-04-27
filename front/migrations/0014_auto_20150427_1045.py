# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0013_auto_20150424_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='cyclist',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 13, 44, 58, 80259, tzinfo=utc), verbose_name='created date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cyclist',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 13, 45, 7, 57353, tzinfo=utc), verbose_name='modified date', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='point',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 13, 45, 13, 61184, tzinfo=utc), verbose_name='created date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='point',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 13, 45, 18, 446259, tzinfo=utc), verbose_name='modified date', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='track',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 13, 45, 28, 606804, tzinfo=utc), verbose_name='created date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='track',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 13, 45, 51, 169417, tzinfo=utc), verbose_name='modified date', auto_now=True),
            preserve_default=False,
        ),
    ]
