# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailqueue', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queuedmail',
            old_name='content',
            new_name='html_content',
        ),
    ]
