# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyclists', '0003_auto_20150527_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='available',
            field=models.BooleanField(default=True, verbose_name='Available'),
        ),
    ]
