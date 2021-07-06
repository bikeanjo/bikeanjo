# -*- coding: utf-8 -*-


import json
from django.db import models, migrations
from django.conf import settings

def load_countries(apps, schema_editor):
    Country = apps.get_model("cities", "Country")
    path = '%s/data/countries.json' % settings.BASE_DIR
    countries = json.load(open(path, 'r'))
    last = Country.objects.latest('id').id

    generator = (Country(id=i + last, name=country['name'], acronym=country['acronym'])
                 for i,country in enumerate(countries, 1)
                 if country['acronym'] != 'BR')
    Country.objects.bulk_create(generator)


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0008_auto_20150916_0539'),
    ]

    operations = [
        migrations.RunPython(load_countries)
    ]
