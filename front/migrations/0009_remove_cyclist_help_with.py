# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0008_auto_20150417_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cyclist',
            name='help_with',
        ),
    ]
