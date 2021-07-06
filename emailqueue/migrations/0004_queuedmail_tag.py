# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailqueue', '0003_auto_20160302_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='queuedmail',
            name='tag',
            field=models.CharField(db_index=True, max_length=64, verbose_name='Tag', blank=True),
        ),
    ]
