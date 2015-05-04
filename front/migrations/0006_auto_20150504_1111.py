# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0005_helpreply'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='helpreply',
            options={'ordering': ['-created_date']},
        ),
        migrations.AddField(
            model_name='helpreply',
            name='rating',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='rating'),
        ),
    ]
