    # -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
from django.db import models, migrations
from django.db.utils import DataError
from django.contrib.gis.geos import Point
from django.conf import settings

NAME = 1
ALIAS = 3
LAT = 4
LON = 5
COUNTRY = 8
TIMEZONE = 17


def load_cities_from_world(apps, schema_editor):
    City = apps.get_model('cities', 'City')
    CityAlias = apps.get_model('cities', 'CityAlias')
    Country = apps.get_model('cities', 'Country')
    path = '%s/data/cities.txt' % settings.BASE_DIR

    City.objects.all().delete()
    countries = dict(Country.objects.values_list('acronym', 'id'))

    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=str('\t'), quotechar=None)
        for row in reader:
            aliases = set(row[ALIAS].decode('utf-8').split(','))
            aliases.add(row[NAME].decode('utf-8'))

            city = City()
            city.name = row[NAME]
            city.country_id = countries.get(row[COUNTRY], None)
            city.tz = row[TIMEZONE]
            city.point = Point(float(row[LON]), float(row[LAT]))
            city.save()

            gen = (CityAlias(city=city, name=alias) for alias in aliases)
            #import ipdb; ipdb.set_trace()
            CityAlias.objects.bulk_create(gen)


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0011_auto_20160314_0811'),
    ]

    operations = [
        migrations.RunPython(load_cities_from_world)
    ]
