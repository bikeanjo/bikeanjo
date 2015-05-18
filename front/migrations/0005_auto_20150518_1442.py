# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0004_auto_20150518_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='modified date')),
                ('title', models.CharField(max_length=128)),
                ('content', models.TextField()),
                ('image', models.ImageField(null=True, upload_to=b'events', blank=True)),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('address', models.CharField(max_length=b'128', verbose_name='address', blank=True)),
                ('address_link', models.CharField(max_length=b'255', verbose_name='address link', blank=True)),
                ('link', models.CharField(max_length=b'255', verbose_name='link', blank=True)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ImageField(null=True, upload_to=b'messages', blank=True),
        ),
    ]
