# -*- coding: utf-8 -*-


from django.db import models, migrations
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cyclists', '0010_normalize_user_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bikeanjo',
            options={'verbose_name': 'Bike Anjo', 'verbose_name_plural': 'Bike anjos'},
        ),
        migrations.AlterModelOptions(
            name='requester',
            options={'verbose_name': 'New cyclist', 'verbose_name_plural': 'New cyclists'},
        ),
        migrations.AlterField(
            model_name='user',
            name='accepted_agreement',
            field=models.BooleanField(default=False, verbose_name='Accepted Terms of Use'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bike_use',
            field=models.CharField(blank=True, max_length=32, verbose_name='Bike use', choices=[(b'everyday', 'Everyday'), (b'just few days a week/month', 'Only a few days per week/month'), (b'once a week', 'Once a week'), (b'no, i use for leisure', 'I only use my bike for leisure or on weekends')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(default=datetime.date.today, null=True, verbose_name='Date of birth'),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='cities.City', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='city_alias',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='cities.CityAlias', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='cities.Country', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='ride_experience',
            field=models.CharField(blank=True, max_length=32, verbose_name='Ride experience', choices=[(b'less than 1 year', 'Less than 1 year'), (b'from 1 to 2 years', 'From 1 to 2 years'), (b'from 2 to 4 years', 'From 2 to 4 years'), (b'more than 4 years', 'More than 4 years'), (b'do not know pedaling yet', "I still don't know how to ride a bike"), (b'no experience in traffic', 'I know how to ride a bike, but have not traffic experience'), (b'already ride a long time', 'I bike for many years now, but not on a daily basis'), (b'use bike almost every day', 'I ride my bike almost every day')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, max_length=32, verbose_name='Role', choices=[(b'bikeanjo', 'Bike Anjo'), (b'requester', 'New cyclist')]),
        ),
    ]
