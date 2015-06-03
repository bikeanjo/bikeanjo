# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0004_auto_20150602_2058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='category',
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(max_length=128, verbose_name='Slug'),
        ),
    ]
