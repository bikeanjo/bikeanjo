# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0005_auto_20150518_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.CharField(default='', max_length=b'64', verbose_name='city'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.IntegerField(default=0, verbose_name='price', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='end date', blank=True),
        ),
    ]
