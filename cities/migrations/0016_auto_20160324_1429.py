# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0015_auto_20160318_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024, verbose_name='Alias name', db_index=True)),
                ('country', models.ForeignKey(to='cities.Country')),
            ],
            options={
                'verbose_name': 'Alias',
                'verbose_name_plural': 'Aliases',
            },
        ),
        migrations.AlterUniqueTogether(
            name='countryalias',
            unique_together=set([('country', 'name')]),
        ),
    ]
