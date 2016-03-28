# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0017_load_countries_alias'),
    ]

    operations = [
        migrations.RunSQL('CREATE INDEX country_countryalias_name_lowercase_like ON cities_countryalias USING BTREE (LOWER(name) varchar_pattern_ops);')
    ]
