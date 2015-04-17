# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0009_remove_cyclist_help_with'),
    ]

    operations = [
        migrations.AddField(
            model_name='cyclist',
            name='help_with',
            field=models.IntegerField(default=0, choices=[(1, 'Advice about safe routes'), (2, 'Follow someone in a ride'), (4, 'Teach someone to ride a bike'), (8, 'Talk in workshop')]),
        ),
    ]
