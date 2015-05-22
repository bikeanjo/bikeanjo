# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0014_auto_20150522_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bikeanjo',
            fields=[
            ],
            options={
                'verbose_name': 'Bikeanjo',
                'proxy': True,
                'verbose_name_plural': 'Bikeanjos',
            },
            bases=('front.user',),
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
            bases=('front.user',),
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ImageField(upload_to=b'messages', null=True, verbose_name='Image', blank=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Title'),
        ),
    ]
