# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='acronym',
            field=models.CharField(default='', max_length=4, verbose_name='Acronym'),
            preserve_default=False,
        ),
    ]
