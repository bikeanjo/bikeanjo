# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slideitem',
            options={'ordering': ['order'], 'verbose_name': 'Slide', 'verbose_name_plural': 'Slides'},
        ),
        migrations.AlterField(
            model_name='slideitem',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]
