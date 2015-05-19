# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0007_contentreadlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='helprequest',
            name='last_reply_date',
        ),
        migrations.AddField(
            model_name='helprequest',
            name='point',
            field=models.ForeignKey(blank=True, to='front.Point', null=True),
        ),
        migrations.AddField(
            model_name='helprequest',
            name='track',
            field=models.ForeignKey(blank=True, to='front.Track', null=True),
        ),
    ]
