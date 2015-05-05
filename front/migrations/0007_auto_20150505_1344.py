# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0006_auto_20150504_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helprequest',
            name='status',
            field=models.CharField(default=b'new', max_length=16, choices=[(b'new', 'New'), (b'canceled', 'Canceled'), (b'attended', 'Attended'), (b'forwarded', 'Forwarded')]),
        ),
    ]
