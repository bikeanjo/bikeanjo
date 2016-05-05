# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0041_auto_20160404_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipforcycling',
            name='content',
            field=models.TextField(verbose_name='Content', blank=True),
        ),
        migrations.AlterField(
            model_name='tipforcycling',
            name='content_en',
            field=models.TextField(null=True, verbose_name='Content', blank=True),
        ),
        migrations.AlterField(
            model_name='tipforcycling',
            name='content_es',
            field=models.TextField(null=True, verbose_name='Content', blank=True),
        ),
        migrations.AlterField(
            model_name='tipforcycling',
            name='content_pt_br',
            field=models.TextField(null=True, verbose_name='Content', blank=True),
        ),
        migrations.AlterField(
            model_name='tipforcycling',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='tipforcycling',
            name='title_en',
            field=models.CharField(max_length=128, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='tipforcycling',
            name='title_es',
            field=models.CharField(max_length=128, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='tipforcycling',
            name='title_pt_br',
            field=models.CharField(max_length=128, null=True, verbose_name='Title', blank=True),
        ),
    ]
