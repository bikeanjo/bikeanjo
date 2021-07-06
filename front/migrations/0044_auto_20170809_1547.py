# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0043_auto_20160404_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='address_fr',
            field=models.CharField(max_length=b'128', null=True, verbose_name='Address', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='content_fr',
            field=models.TextField(null=True, verbose_name='Content', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='price_fr',
            field=models.CharField(max_length=b'128', null=True, verbose_name='Price', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='subscription_link_fr',
            field=models.CharField(max_length=b'255', null=True, verbose_name='Link', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='title_fr',
            field=models.CharField(max_length=128, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='testimony',
            name='message_fr',
            field=models.CharField(max_length=255, null=True, verbose_name='Message'),
        ),
        migrations.AddField(
            model_name='tipforcycling',
            name='content_fr',
            field=models.TextField(null=True, verbose_name='Content', blank=True),
        ),
        migrations.AddField(
            model_name='tipforcycling',
            name='title_fr',
            field=models.CharField(max_length=128, null=True, verbose_name='Title', blank=True),
        ),
    ]
