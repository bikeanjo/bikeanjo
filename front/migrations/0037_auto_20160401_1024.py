# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0036_auto_20160330_1902'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Event category', 'verbose_name_plural': 'Event categories'},
        ),
        migrations.AlterModelOptions(
            name='helpreply',
            options={'ordering': ['-created_date'], 'verbose_name': 'Reply to the request', 'verbose_name_plural': 'Replies to the request'},
        ),
        migrations.AlterModelOptions(
            name='tipforcycling',
            options={'verbose_name': 'Cycling tip', 'verbose_name_plural': 'Cycling tips'},
        ),
        migrations.AlterModelOptions(
            name='track',
            options={'verbose_name': 'Route', 'verbose_name_plural': 'Routes'},
        ),
        migrations.AlterField(
            model_name='contactmessage',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='contactmessage',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='event',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='event',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='helpreply',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='helpreply',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='closed_by',
            field=models.CharField(blank=True, max_length=12, verbose_name='Closed by', choices=[(b'bikeanjo', 'Bike Anjo'), (b'requester', 'New cyclist')]),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='helprequest',
            name='status',
            field=models.CharField(default=b'new', max_length=16, verbose_name='Status', choices=[(b'new', 'New'), (b'open', 'Open'), (b'attended', 'Attended'), (b'finalized', 'Finished'), (b'canceled', 'Canceled'), (b'rejected', 'Rejected')]),
        ),
        migrations.AlterField(
            model_name='match',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='match',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='message',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='message',
            name='target_roles',
            field=models.CharField(default=b'all', max_length=16, verbose_name='Target', choices=[(b'all', 'All'), (b'bikeanjo', 'Bike Anjo'), (b'requester', 'New cyclist')]),
        ),
        migrations.AlterField(
            model_name='point',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='point',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='readedmessage',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='readedmessage',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='testimony',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='testimony',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='tipforcycling',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='tipforcycling',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
        migrations.AlterField(
            model_name='tipforcycling',
            name='target',
            field=models.CharField(default=b'all', max_length=16, verbose_name='Target', choices=[(b'all', 'All'), (b'bikeanjo', 'Bike Anjo'), (b'requester', 'New cyclist')]),
        ),
        migrations.AlterField(
            model_name='track',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='track',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date of change'),
        ),
    ]
