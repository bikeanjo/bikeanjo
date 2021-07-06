# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0023_readedmessage'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='readedmessage',
            unique_together=set([('user', 'message')]),
        ),
    ]
