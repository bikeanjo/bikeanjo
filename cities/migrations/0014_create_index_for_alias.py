# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0013_load_extension_fuzzystrmatch'),
    ]

    operations = [
        migrations.RunSQL('CREATE INDEX city_cityalias_alias_lowercase_like ON cities_cityalias USING BTREE (LOWER(name) varchar_pattern_ops);')
    ]
