# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0027_auto_20150708_0835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Event category', 'verbose_name_plural': 'Events categories'},
        ),
        migrations.AlterModelOptions(
            name='subscriber',
            options={'verbose_name': 'Newsletter', 'verbose_name_plural': 'Newsletters'},
        ),
    ]
