# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0026_auto_20150708_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.CharField(max_length=128, verbose_name='Price', blank=True),
        ),
    ]
