# -*- coding: utf-8 -*-


from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django.utils.timezone
from django.conf import settings
import front.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentReadLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Content read log',
                'verbose_name_plural': 'Content read logs',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('image', models.ImageField(upload_to=b'events', null=True, verbose_name='Image', blank=True)),
                ('start_date', models.DateTimeField(verbose_name='Start date')),
                ('end_date', models.DateTimeField(null=True, verbose_name='End date', blank=True)),
                ('city', models.CharField(max_length=64, verbose_name='City')),
                ('address', models.CharField(max_length=128, verbose_name='Address', blank=True)),
                ('address_link', models.CharField(max_length=255, verbose_name='Address link', blank=True)),
                ('link', models.CharField(max_length=255, verbose_name='Link', blank=True)),
                ('price', models.IntegerField(default=0, verbose_name='Price', blank=True)),
            ],
            options={
                'ordering': ['-created_date'],
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
            bases=(models.Model, front.models.ReadedAnnotationMixin),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('message', models.CharField(max_length=255, verbose_name='Message')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedbacks',
            },
        ),
        migrations.CreateModel(
            name='HelpReply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('message', models.TextField(verbose_name='Message')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='HelpRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('help_with', models.IntegerField(default=0, verbose_name='Help with')),
                ('status', models.CharField(default=b'new', max_length=16, verbose_name='Status', choices=[(b'new', 'New'), (b'open', 'Open'), (b'attended', 'Attended'), (b'finalized', 'Finalized'), (b'canceled', 'Canceled')])),
                ('requester_access', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Access date', editable=False)),
                ('bikeanjo_access', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Access date', editable=False)),
                ('requester_rating', models.PositiveSmallIntegerField(default=0, verbose_name='Rating')),
                ('requester_eval', models.TextField(verbose_name='Evaluation', blank=True)),
                ('bikeanjo', models.ForeignKey(related_name='helpbikeanjo_set', to=settings.AUTH_USER_MODEL, null=True)),
                ('requester', models.ForeignKey(related_name='helprequested_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Help request',
                'verbose_name_plural': 'Help requests',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('score', models.FloatField(default=0, verbose_name='Score')),
                ('rejected_date', models.DateTimeField(null=True, verbose_name='Rejected date')),
                ('reason', models.CharField(max_length=128, verbose_name='Reason', blank=True)),
                ('bikeanjo', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('helprequest', models.ForeignKey(to='front.HelpRequest')),
            ],
            options={
                'verbose_name': 'Match',
                'verbose_name_plural': 'Matches',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('image', models.ImageField(upload_to=b'messages', null=True, verbose_name='Image', blank=True)),
            ],
            options={
                'ordering': ['-created_date'],
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(models.Model, front.models.ReadedAnnotationMixin),
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('address', models.CharField(max_length=128, verbose_name='Address')),
                ('coords', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Point',
                'verbose_name_plural': 'Points',
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('start', models.CharField(max_length=128, verbose_name='Start')),
                ('end', models.CharField(max_length=128, verbose_name='End')),
                ('track', django.contrib.gis.db.models.fields.LineStringField(srid=4326)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Track',
                'verbose_name_plural': 'Tracks',
            },
        ),
        migrations.AddField(
            model_name='helprequest',
            name='track',
            field=models.ForeignKey(blank=True, to='front.Track', null=True),
        ),
        migrations.AddField(
            model_name='helpreply',
            name='helprequest',
            field=models.ForeignKey(to='front.HelpRequest'),
        ),
    ]
