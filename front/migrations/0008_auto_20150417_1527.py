# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0007_auto_20150417_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='cyclist',
            name='initiatives',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='cyclist',
            name='bike_use',
            field=models.CharField(blank=True, max_length=32, choices=[(b'everyday', 'Everyday'), (b'just few days a week/month', 'Just few days a week/month'), (b'once a week', 'Once a week'), (b'no, i use for leisure', 'No, I use for leisure')]),
        ),
        migrations.AlterField(
            model_name='cyclist',
            name='gender',
            field=models.CharField(max_length=24, blank=True),
        ),
        migrations.AlterField(
            model_name='cyclist',
            name='ride_experience',
            field=models.CharField(blank=True, max_length=32, choices=[(b'less than 1 year', 'Less than 1 year'), (b'from 1 to 2 years', 'From 1 to 2 years'), (b'from 2 to 4 years', 'From 2 to 4 years'), (b'more than 4 years', 'More than 4 years')]),
        ),
    ]
