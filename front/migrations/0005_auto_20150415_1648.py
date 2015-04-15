# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0004_auto_20150415_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='track',
            field=django.contrib.gis.db.models.fields.LineStringField(srid=4326),
        ),
    ]
