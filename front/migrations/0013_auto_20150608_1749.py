# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0012_auto_20150608_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='token',
            field=models.CharField(default='', verbose_name='token', max_length=64, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscriber',
            name='valid',
            field=models.BooleanField(default=False, verbose_name='valid'),
        ),
    ]
