# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0029_contactmessage_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='helprequest',
            name='closed_by',
            field=models.CharField(blank=True, max_length=12, verbose_name='Closed by', choices=[(b'bikeanjo', 'Bikeanjo'), (b'requester', 'Requester')]),
        ),
    ]
