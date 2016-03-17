# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0014_create_index_for_alias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='acronym',
            field=models.CharField(max_length=4, verbose_name='Acronym', db_index=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Name', db_index=True),
        ),
    ]
