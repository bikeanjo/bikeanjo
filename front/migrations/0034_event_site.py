# -*- coding: utf-8 -*-


from django.db import models, migrations
import front.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('front', '0033_auto_20151001_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='site',
            field=models.ForeignKey(default=front.models.default_to_first_site, to='sites.Site'),
        ),
    ]
