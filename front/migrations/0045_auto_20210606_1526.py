# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0044_auto_20170809_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helprequest',
            name='status',
            field=models.CharField(default=b'new', max_length=16, verbose_name='Status', choices=[(b'new', 'New'), (b'open', 'Open'), (b'attended', 'Attended'), (b'finalized', 'Finished'), (b'canceled', 'Canceled'), (b'rejected', 'Rejected'), (b'eba', 'Closed by EBA')]),
        ),
    ]
