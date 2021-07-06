# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0009_testimony'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helprequest',
            name='status',
            field=models.CharField(default=b'new', max_length=16, verbose_name='Status', choices=[(b'new', 'New'), (b'open', 'Open'), (b'attended', 'Attended'), (b'finalized', 'Finalized'), (b'canceled', 'Canceled'), (b'rejected', 'Rejected')]),
        ),
        migrations.AlterUniqueTogether(
            name='match',
            unique_together=set([('bikeanjo', 'helprequest')]),
        ),
    ]
