# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0003_auto_20150430_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helprequest',
            name='status',
            field=models.CharField(default=b'new', max_length=16, choices=[(b'new', 'New'), (b'assigned', 'Assigned'), (b'canceled', 'Canceled'), (b'finished', 'Finished')]),
        ),
    ]
