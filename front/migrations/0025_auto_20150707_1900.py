# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import re
from django.conf import settings
from django.db import models, migrations


def load_flatpages_from_template(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    pattern = re.compile(r'{% *block *content *%}([^{]+){% *endblock *%}', re.MULTILINE)

    content = open(os.path.join(settings.BASE_DIR, 'templates/about.html')).read()
    content = pattern.search(content).group(1)

    site = Site.objects.first()
    if not site:
        site = Site.objects.create(name='bikeanjo.org', domain='bikeanjo.org')

    Site.objects.first().flatpage_set.create(
        title='Sobre nós',
        url='/about/sobre-nos/',
        content=content,
    )

    content = open(os.path.join(settings.BASE_DIR, 'templates/how_it_works.html')).read()
    content = pattern.search(content).group(1)
    Site.objects.first().flatpage_set.create(
        title='Como funciona',
        url='/work/como-funciona/',
        content=content,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0024_auto_20150706_2159'),
    ]

    operations = [
        migrations.RunPython(load_flatpages_from_template)
    ]
