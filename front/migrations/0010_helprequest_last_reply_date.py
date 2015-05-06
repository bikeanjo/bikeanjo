# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0009_remove_helprequest_last_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='helprequest',
            name='last_reply_date',
            field=models.DateTimeField(verbose_name='last reply date', null=True, editable=False),
        ),
    ]
