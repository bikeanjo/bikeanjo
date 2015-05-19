# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0010_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='modified date')),
                ('score', models.IntegerField(default=0)),
                ('rejected_date', models.DateTimeField(null=True)),
                ('reason', models.CharField(max_length=128)),
                ('bikeanjo', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('helprequest', models.ForeignKey(to='front.HelpRequest')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
