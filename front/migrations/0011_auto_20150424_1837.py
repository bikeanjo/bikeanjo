# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def assign_user_to_point(apps, schema_editor):
    Point = apps.get_model("front", "Point")
    for point in Point.objects.all():
        point.user = point.cyclist.user
        point.save()


def assign_user_to_track(apps, schema_editor):
    Track = apps.get_model("front", "Track")
    for track in Track.objects.all():
        track.user = track.cyclist.user
        track.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('front', '0010_cyclist_help_with'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='cyclist',
            name='help_with',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cyclist',
            name='ride_experience',
            field=models.CharField(blank=True, max_length=32, choices=[(b'less than 1 year', 'Less than 1 year'), (b'from 1 to 2 years', 'From 1 to 2 years'), (b'from 2 to 4 years', 'From 2 to 4 years'), (b'more than 4 years', 'More than 4 years'), (b'do not know pedaling yet', 'I do not know pedaling yet'), (b'no experience in traffic', 'I know cycling, but have no experience in traffic'), (b'already ride a long time', 'Already ride a long time but not daily'), (b'use bike almost every day', 'I use bike almost every day')]),
        ),
        migrations.RunPython(assign_user_to_point),
        migrations.RunPython(assign_user_to_track),
    ]
