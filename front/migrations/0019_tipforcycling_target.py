# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0018_auto_20150706_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipforcycling',
            name='target',
            field=models.CharField(default=b'all', max_length=128, verbose_name='Title', choices=[(b'all', 'All'), (b'bikeanjo', 'Bikeanjo'), (b'requester', 'Requester')]),
        ),
    ]
