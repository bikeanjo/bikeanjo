# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0021_auto_20150706_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentreadlog',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='contentreadlog',
            name='user',
        ),
        migrations.DeleteModel(
            name='ContentReadLog',
        ),
    ]
