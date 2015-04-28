# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.contrib.auth.models
import django.contrib.gis.db.models.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('country', models.CharField(max_length=32, blank=True)),
                ('city', models.CharField(max_length=32, blank=True)),
                ('gender', models.CharField(max_length=24, blank=True)),
                ('birthday', models.DateField(default=datetime.date.today, null=True)),
                ('ride_experience', models.CharField(blank=True, max_length=32, choices=[(b'less than 1 year', 'Less than 1 year'), (b'from 1 to 2 years', 'From 1 to 2 years'), (b'from 2 to 4 years', 'From 2 to 4 years'), (b'more than 4 years', 'More than 4 years'), (b'do not know pedaling yet', 'I do not know pedaling yet'), (b'no experience in traffic', 'I know cycling, but have no experience in traffic'), (b'already ride a long time', 'Already ride a long time but not daily'), (b'use bike almost every day', 'I use bike almost every day')])),
                ('bike_use', models.CharField(blank=True, max_length=32, choices=[(b'everyday', 'Everyday'), (b'just few days a week/month', 'Just few days a week/month'), (b'once a week', 'Once a week'), (b'no, i use for leisure', 'No, I use for leisure')])),
                ('help_with', models.IntegerField(default=0)),
                ('initiatives', models.CharField(max_length=256, blank=True)),
                ('role', models.CharField(blank=True, max_length=32, choices=[(b'volunteer', 'Volunteer'), (b'requester', 'Requester')])),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='HelpRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='modified date')),
                ('help_with', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'new', max_length=16, choices=[(b'new', 'New'), (b'assigned', 'Assigned'), (b'canceled', 'Canceled'), (b'attended', 'Attended')])),
                ('requester', models.ForeignKey(related_name='helprequested_set', to=settings.AUTH_USER_MODEL)),
                ('volunteer', models.ForeignKey(related_name='helpvolunteered_set', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='modified date')),
                ('address', models.CharField(max_length=128)),
                ('coords', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='modified date')),
                ('start', models.CharField(max_length=128)),
                ('end', models.CharField(max_length=128)),
                ('track', django.contrib.gis.db.models.fields.LineStringField(srid=4326)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
