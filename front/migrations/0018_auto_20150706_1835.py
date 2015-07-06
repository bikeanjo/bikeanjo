# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0017_tipforcycling'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipforcycling',
            name='link',
            field=models.CharField(max_length=b'255', verbose_name='Link', blank=True),
        ),
        migrations.AlterField(
            model_name='tipforcycling',
            name='image',
            field=models.ImageField(upload_to=b'tips', null=True, verbose_name='Image', blank=True),
        ),
    ]
