# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailqueue', '0002_auto_20160302_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='queuedmail',
            name='text_content',
            field=models.TextField(default='', verbose_name='Text Content'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='queuedmail',
            name='html_content',
            field=models.TextField(verbose_name='HTML Content'),
        ),
    ]
