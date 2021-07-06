# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0015_auto_20160318_1537'),
        ('cyclists', '0008_auto_20160318_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.ForeignKey(to='cities.City', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='city_alias',
            field=models.ForeignKey(to='cities.CityAlias', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.ForeignKey(to='cities.Country', null=True),
        ),
    ]
