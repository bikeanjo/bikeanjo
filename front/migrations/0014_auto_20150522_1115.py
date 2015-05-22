# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0013_auto_20150519_1852'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contentreadlog',
            options={'verbose_name': 'Content read log', 'verbose_name_plural': 'Content read logs'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-created_date'], 'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': 'Feedback', 'verbose_name_plural': 'Feedbacks'},
        ),
        migrations.AlterModelOptions(
            name='helprequest',
            options={'verbose_name': 'Help request', 'verbose_name_plural': 'Help requests'},
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name': 'Match', 'verbose_name_plural': 'Matches'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-created_date'], 'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.AlterModelOptions(
            name='point',
            options={'verbose_name': 'Point', 'verbose_name_plural': 'Points'},
        ),
        migrations.AlterModelOptions(
            name='track',
            options={'verbose_name': 'Track', 'verbose_name_plural': 'Tracks'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'User'},
        ),
        migrations.AlterField(
            model_name='contentreadlog',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.CharField(max_length=b'128', verbose_name='Address', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='address_link',
            field=models.CharField(max_length=b'255', verbose_name='Address link', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='city',
            field=models.CharField(max_length=b'64', verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='event',
            name='content',
            field=models.TextField(verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='event',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='End date', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to=b'events', null=True, verbose_name='Image', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='link',
            field=models.CharField(max_length=b'255', verbose_name='Link', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Price', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(verbose_name='Start date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='message',
            field=models.CharField(max_length=255, verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified date'),
        ),
        migrations.AlterField(
            model_name='helpreply',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='helpreply',
            name='message',
            field=models.TextField(verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='helpreply',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified date'),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='bikeanjo_access',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Access date', editable=False),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='help_with',
            field=models.IntegerField(default=0, verbose_name='Help with'),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified date'),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='requester_access',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Access date', editable=False),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='requester_eval',
            field=models.TextField(verbose_name='Evaluation', blank=True),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='requester_rating',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='status',
            field=models.CharField(default=b'new', max_length=16, verbose_name='Status', choices=[(b'new', 'New'), (b'open', 'Open'), (b'attended', 'Attended'), (b'finalized', 'Finalized'), (b'canceled', 'Canceled')]),
        ),
        migrations.AlterField(
            model_name='match',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='match',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified date'),
        ),
        migrations.AlterField(
            model_name='match',
            name='reason',
            field=models.CharField(max_length=128, verbose_name='Reason', blank=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='rejected_date',
            field=models.DateTimeField(null=True, verbose_name='Rejected date'),
        ),
        migrations.AlterField(
            model_name='match',
            name='score',
            field=models.FloatField(default=0, verbose_name='Score'),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='message',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified date'),
        ),
        migrations.AlterField(
            model_name='point',
            name='address',
            field=models.CharField(max_length=128, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='point',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='point',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified date'),
        ),
        migrations.AlterField(
            model_name='track',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='track',
            name='end',
            field=models.CharField(max_length=128, verbose_name='End'),
        ),
        migrations.AlterField(
            model_name='track',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified date'),
        ),
        migrations.AlterField(
            model_name='track',
            name='start',
            field=models.CharField(max_length=128, verbose_name='Start'),
        ),
        migrations.AlterField(
            model_name='user',
            name='accepted_agreement',
            field=models.BooleanField(default=False, verbose_name='Accepted agreement'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bike_use',
            field=models.CharField(blank=True, max_length=32, verbose_name='Bike use', choices=[(b'everyday', 'Everyday'), (b'just few days a week/month', 'Just few days a week/month'), (b'once a week', 'Once a week'), (b'no, i use for leisure', 'No, I use for leisure')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(default=datetime.date.today, null=True, verbose_name='Birthday'),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=32, verbose_name='City', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(max_length=32, verbose_name='Country', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=24, verbose_name='Gender', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='help_with',
            field=models.IntegerField(default=0, verbose_name='Help with'),
        ),
        migrations.AlterField(
            model_name='user',
            name='initiatives',
            field=models.CharField(max_length=256, verbose_name='Initiatives', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='ride_experience',
            field=models.CharField(blank=True, max_length=32, verbose_name='Ride experience', choices=[(b'less than 1 year', 'Less than 1 year'), (b'from 1 to 2 years', 'From 1 to 2 years'), (b'from 2 to 4 years', 'From 2 to 4 years'), (b'more than 4 years', 'More than 4 years'), (b'do not know pedaling yet', 'I do not know pedaling yet'), (b'no experience in traffic', 'I know cycling, but have no experience in traffic'), (b'already ride a long time', 'Already ride a long time but not daily'), (b'use bike almost every day', 'I use bike almost every day')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, max_length=32, verbose_name='Role', choices=[(b'bikeanjo', 'Bikeanjo'), (b'requester', 'Requester')]),
        ),
    ]
