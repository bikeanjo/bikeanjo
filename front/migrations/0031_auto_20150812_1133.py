# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0030_helprequest_closed_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='helpreply',
            options={'ordering': ['-created_date'], 'verbose_name': 'Help reply', 'verbose_name_plural': 'Help replies'},
        ),
        migrations.AddField(
            model_name='helprequest',
            name='message',
            field=models.TextField(default='', verbose_name='Message'),
            preserve_default=False,
        ),
    ]
