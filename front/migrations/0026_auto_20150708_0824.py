# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0025_auto_20150707_1900'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='link',
            new_name='subscription_link',
        ),
    ]
