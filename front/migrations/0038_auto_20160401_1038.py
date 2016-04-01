# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0037_auto_20160401_1024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='city',
            new_name='v1_city',
        ),
    ]
