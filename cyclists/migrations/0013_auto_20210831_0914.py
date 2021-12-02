# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2021-08-31 12:14
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cyclists', '0012_auto_20170809_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bike_use',
            field=models.CharField(blank=True, choices=[('everyday', 'Everyday'), ('just few days a week/month', 'Only a few days per week/month'), ('once a week', 'Once a week'), ('no, i use for leisure', 'I only use my bike for leisure or on weekends')], max_length=32, verbose_name='Bike use'),
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('pt-br', 'Brazilian Portuguese'), ('es', 'Spanish'), ('en', 'English'), ('fr', 'French')], default='pt-br', max_length=8, verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='user',
            name='ride_experience',
            field=models.CharField(blank=True, choices=[('less than 1 year', 'Less than 1 year'), ('from 1 to 2 years', 'From 1 to 2 years'), ('from 2 to 4 years', 'From 2 to 4 years'), ('more than 4 years', 'More than 4 years'), ('do not know pedaling yet', "I still don't know how to ride a bike"), ('no experience in traffic', 'I know how to ride a bike, but have not traffic experience'), ('already ride a long time', 'I bike for many years now, but not on a daily basis'), ('use bike almost every day', 'I ride my bike almost every day')], max_length=32, verbose_name='Ride experience'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('bikeanjo', 'Bike Anjo'), ('requester', 'New cyclist')], max_length=32, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username'),
        ),
    ]