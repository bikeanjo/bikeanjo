# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('front', '0014_auto_20150427_1045'),
    ]

    operations = [
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
    ]
