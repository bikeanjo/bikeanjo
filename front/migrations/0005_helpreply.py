# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0004_auto_20150430_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpReply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='modified date')),
                ('message', models.TextField(verbose_name='message')),
                ('intention', models.CharField(default=b'answer', max_length=16, verbose_name='intention', choices=[(b'answer', 'Answer'), (b'finish', 'Finish'), (b'cancel', 'Cancel')])),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('helprequest', models.ForeignKey(to='front.HelpRequest')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
