# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='helprequest',
            field=models.ForeignKey(blank=True, to='front.HelpRequest', null=True),
        ),
    ]
