# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cyclist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(blank=True, max_length=32, verbose_name='role', choices=[(b'volunteer', 'Volunteer'), (b'recipient', 'Recipient')])),
                ('bio', models.CharField(max_length=140, verbose_name='biography', blank=True)),
                ('date_of_birth', models.DateField(default=datetime.datetime(1984, 10, 22, 0, 0), null=True, verbose_name='date of birth')),
                ('gender', models.CharField(blank=True, max_length=1, verbose_name='gender', choices=[(b'M', 'Male'), (b'F', 'Female')])),
                ('phone', models.CharField(max_length=32, verbose_name='phone number', blank=True)),
                ('years_experience', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='years of experience')),
                ('address', models.CharField(max_length=64, verbose_name='address', blank=True)),
                ('address_number', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='number')),
                ('address_complement', models.CharField(max_length=16, verbose_name='complement', blank=True)),
                ('locality', models.CharField(max_length=32, verbose_name='locality', blank=True)),
                ('state', models.CharField(max_length=32, verbose_name='state', blank=True)),
                ('level_in_mechanics', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Mechanics')),
                ('level_in_security', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Security')),
                ('level_in_legislation', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Legislation')),
                ('level_in_routes', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Routes')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='cyclist',
            name='services',
            field=models.ManyToManyField(db_constraint='provide services', to='front.Service', blank=True),
        ),
        migrations.AddField(
            model_name='cyclist',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
