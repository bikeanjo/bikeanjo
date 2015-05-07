# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0010_helprequest_last_reply_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='helprequest',
            name='accepted',
            field=models.BooleanField(default=False, verbose_name='pedido aceito'),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='status',
            field=models.CharField(default=b'new', max_length=16, choices=[(b'new', 'New'), (b'canceled', 'Canceled'), (b'attended', 'Attended')]),
        ),
    ]
