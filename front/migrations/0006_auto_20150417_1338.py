# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0005_auto_20150415_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cyclist',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='cyclist',
            name='state',
        ),
        migrations.AddField(
            model_name='cyclist',
            name='bike_use',
            field=models.CharField(blank=True, max_length=32, choices=[(b'everyday', 'everyday'), (b'few days a week', 'Just few days a week/month'), (b'once a week', 'Once a week'), (b'only for leisure', 'No, I use for leisure')]),
        ),
        migrations.AddField(
            model_name='cyclist',
            name='ride_experience',
            field=models.CharField(blank=True, max_length=32, choices=[(b'lt1', 'Less than 1 year'), (b'[1,2]', 'From 1 to 2 years'), (b'[2,4]', 'From 2 to 4 years'), (b'gt4', 'More than 4 years')]),
        ),
    ]
