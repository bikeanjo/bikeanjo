# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cyclist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birthday', models.DateField(default=datetime.date.today, null=True)),
                ('city', models.CharField(max_length=32, blank=True)),
                ('country', models.CharField(max_length=32, blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, choices=[(b'M', 'Male'), (b'F', 'Female')])),
                ('help_with', models.CharField(blank=True, max_length=16, choices=[(b'advice', 'Advice about safe routes'), (b'escort', 'Follow someone in a ride'), (b'teach', 'Teach someone to ride a bike'), (b'workshop', 'Talk in workshop')])),
                ('phone', models.CharField(max_length=32, blank=True)),
                ('role', models.CharField(blank=True, max_length=32, choices=[(b'volunteer', 'Volunteer'), (b'requester', 'Requester')])),
                ('state', models.CharField(max_length=32, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=128)),
                ('coords', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('cyclist', models.ForeignKey(to='front.Cyclist')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('track', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
                ('cyclist', models.ForeignKey(to='front.Cyclist')),
            ],
        ),
    ]
