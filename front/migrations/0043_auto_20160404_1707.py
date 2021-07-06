# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0042_auto_20160404_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimony',
            name='message_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Message'),
        ),
        migrations.AddField(
            model_name='testimony',
            name='message_es',
            field=models.CharField(max_length=255, null=True, verbose_name='Message'),
        ),
        migrations.AddField(
            model_name='testimony',
            name='message_pt_br',
            field=models.CharField(max_length=255, null=True, verbose_name='Message'),
        ),
    ]
