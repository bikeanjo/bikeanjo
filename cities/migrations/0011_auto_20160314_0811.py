# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0010_auto_20160311_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cityalias',
            name='alias',
            field=models.CharField(max_length=1024, verbose_name='Alias', db_index=True),
        ),
    ]
