# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0028_auto_20150710_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='name',
            field=models.CharField(default='Inserted by migration', max_length=128, verbose_name='Name'),
            preserve_default=False,
        ),
    ]
