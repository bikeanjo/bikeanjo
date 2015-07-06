# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0016_contactmessage_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipForCycling',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('image', models.ImageField(upload_to=b'events', null=True, verbose_name='Image', blank=True)),
            ],
            options={
                'verbose_name': 'Tip for cycling',
                'verbose_name_plural': 'Tips for cycling',
            },
        ),
    ]
