# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0018_countryalias_name_index'),
        ('front', '0035_auto_20160323_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='target_city',
            field=models.ForeignKey(blank=True, to='cities.City', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='target_country',
            field=models.ForeignKey(blank=True, to='cities.Country', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='target_roles',
            field=models.CharField(default=b'all', max_length=16, verbose_name='Target', choices=[(b'all', 'All'), (b'bikeanjo', 'Bikeanjo'), (b'requester', 'Requester')]),
        ),
    ]
