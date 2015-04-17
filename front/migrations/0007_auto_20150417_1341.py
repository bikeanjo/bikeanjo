# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0006_auto_20150417_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cyclist',
            name='gender',
            field=models.CharField(blank=True, max_length=24, choices=[(b'male', 'Male'), (b'female', 'Female')]),
        ),
    ]
