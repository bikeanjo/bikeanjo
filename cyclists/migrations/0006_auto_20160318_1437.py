# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyclists', '0005_auto_20150831_1833'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='city',
            new_name='v1_city',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='country',
            new_name='v1_country',
        ),
    ]
