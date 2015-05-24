# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
import django.core.validators
import django.contrib.auth.models


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
                ('country', models.CharField(max_length=32, verbose_name='Country', blank=True)),
                ('city', models.CharField(max_length=32, verbose_name='City', blank=True)),
                ('gender', models.CharField(max_length=24, verbose_name='Gender', blank=True)),
                ('birthday', models.DateField(default=datetime.date.today, null=True, verbose_name='Birthday')),
                ('ride_experience', models.CharField(blank=True, max_length=32, verbose_name='Ride experience', choices=[(b'less than 1 year', 'Less than 1 year'), (b'from 1 to 2 years', 'From 1 to 2 years'), (b'from 2 to 4 years', 'From 2 to 4 years'), (b'more than 4 years', 'More than 4 years'), (b'do not know pedaling yet', 'I do not know pedaling yet'), (b'no experience in traffic', 'I know cycling, but have no experience in traffic'), (b'already ride a long time', 'Already ride a long time but not daily'), (b'use bike almost every day', 'I use bike almost every day')])),
                ('bike_use', models.CharField(blank=True, max_length=32, verbose_name='Bike use', choices=[(b'everyday', 'Everyday'), (b'just few days a week/month', 'Just few days a week/month'), (b'once a week', 'Once a week'), (b'no, i use for leisure', 'No, I use for leisure')])),
                ('help_with', models.IntegerField(default=0, verbose_name='Help with')),
                ('initiatives', models.CharField(max_length=256, verbose_name='Initiatives', blank=True)),
                ('role', models.CharField(blank=True, max_length=32, verbose_name='Role', choices=[(b'bikeanjo', 'Bikeanjo'), (b'requester', 'Requester')])),
                ('accepted_agreement', models.BooleanField(default=False, verbose_name='Accepted agreement')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Bikeanjo',
            fields=[
            ],
            options={
                'verbose_name': 'Bikeanjo',
                'proxy': True,
                'verbose_name_plural': 'Bikeanjos',
            },
            bases=('cyclists.user',),
        ),
        migrations.CreateModel(
            name='Requester',
            fields=[
            ],
            options={
                'verbose_name': 'Requester',
                'proxy': True,
                'verbose_name_plural': 'Requesters',
            },
            bases=('cyclists.user',),
        ),
    ]
