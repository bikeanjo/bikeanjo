# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0020_auto_20150706_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipforcycling',
            name='target',
            field=models.CharField(default=b'all', max_length=16, verbose_name='Target', choices=[(b'all', 'All'), (b'bikeanjo', 'Bikeanjo'), (b'requester', 'Requester')]),
        ),
    ]
