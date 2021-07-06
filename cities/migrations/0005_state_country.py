# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0004_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='country',
            field=models.ForeignKey(default=1, to='cities.Country'),
            preserve_default=False,
        ),
    ]
