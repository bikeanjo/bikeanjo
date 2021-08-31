# -*- coding: utf-8 -*-

import csv
from django.db import models, migrations
from django.conf import settings

NAME1 = 1
NAME2 = 2
ALIAS = 3
CODE = 8


def load_country_aliases(apps, schema_editor):
    Country = apps.get_model('cities', 'Country')
    CountryAlias = apps.get_model('cities', 'CountryAlias')
    path = '%s/data/countriesAlias.tsv' % settings.BASE_DIR

    countries = dict(Country.objects.values_list('acronym', 'id'))
    last_id = max(countries.values())

    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=str('\t'), quotechar=None)

        for row in reader:
            aliases = set(row[ALIAS].split(','))
            aliases.add(row[NAME1])
            aliases.add(row[NAME2])

            country_code = row[CODE]
            if country_code not in countries:
                last_id += 1
                Country.objects.create(id=last_id, name=row[NAME1], acronym=country_code)
                countries[country_code] = last_id

            country_id = countries.get(country_code)
            gen = (CountryAlias(country_id=country_id, name=alias) for alias in aliases)
            CountryAlias.objects.bulk_create(gen)


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0016_auto_20160324_1429'),
    ]

    operations = [
        migrations.RunPython(load_country_aliases),
    ]
