# -*- coding: utf-8 -*-

import re
import sys
import string
import unicodedata

from django.db.models import Q
from django.db import models, migrations

def normalize_user_location(apps, schema_editor):
    # load models
    User = apps.get_model('cyclists', 'User')
    Country = apps.get_model('cities', 'Country')
    CityAlias = apps.get_model('cities', 'CityAlias')

    brasil = Country.objects.filter(countryalias__name__lowermatch='Brasil').first()

    # First, the fast
    changes = User.objects.filter(v1_country__iregex='bra[zs]i', country=None).update(country=brasil)
    sys.stdout.write('(p x %d)' % changes)

    # The slow for countries
    countries = set(User.objects.exclude(v1_country='')\
                                .filter(country=None)\
                                .values_list('v1_country', flat=True))

    for name in countries:
        country = Country.objects.filter(countryalias__name__lowermatch=name).distinct()

        if country.count() == 1:
            changes = User.objects.filter(v1_country=name).update(country=country.first())
            sys.stdout.write(' + (p x %d)' % changes)
        else:
            sys.stdout.write('-')

    # The slow for countries
    cities = set(User.objects.exclude(v1_city__regex='^\s*$')
                     .filter(city=None)
                     .values_list('v1_city', flat=True))

    def levenshtein_ordered_qs(qs, value):
        field = '"%s"."name"' % CityAlias._meta.db_table
        function = 'levenshtein(%s, %s)' % ("%s", field)
        qs = qs.extra(
            select={'weight': function, },
            select_params=(value,)
        ).distinct().order_by('weight')
        return qs

    punc_pattern = re.compile(' *[%s]+ *' % re.escape(string.punctuation))
    for v1_name in cities:
        name = ' '.join(v1_name.split())
        name = punc_pattern.split(name)[0].strip()
        clean = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')

        qs = CityAlias.objects\
                      .select_related('city')\
                      .filter(Q(name__lowermatch=name) | Q(name__lowermatch=clean))
        obj = levenshtein_ordered_qs(qs, name).first()

        if obj:
            User.objects.filter(v1_city=v1_name)\
                        .update(city_alias=obj, city=obj.city)


class Migration(migrations.Migration):

    dependencies = [
        ('cyclists', '0009_auto_20160318_1537'),
        ('cities', '0018_countryalias_name_index'),
    ]

    operations = [
        migrations.RunPython(normalize_user_location)
    ]
