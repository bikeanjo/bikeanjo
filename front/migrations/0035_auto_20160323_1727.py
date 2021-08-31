# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0034_event_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='address_en',
            field=models.CharField(max_length=128, null=True, verbose_name='Address', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='address_es',
            field=models.CharField(max_length=128, null=True, verbose_name='Address', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='address_pt_br',
            field=models.CharField(max_length=128, null=True, verbose_name='Address', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='content_en',
            field=models.TextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='event',
            name='content_es',
            field=models.TextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='event',
            name='content_pt_br',
            field=models.TextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='event',
            name='price_en',
            field=models.CharField(max_length=128, null=True, verbose_name='Price', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='price_es',
            field=models.CharField(max_length=128, null=True, verbose_name='Price', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='price_pt_br',
            field=models.CharField(max_length=128, null=True, verbose_name='Price', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='subscription_link_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Link', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='subscription_link_es',
            field=models.CharField(max_length=255, null=True, verbose_name='Link', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='subscription_link_pt_br',
            field=models.CharField(max_length=255, null=True, verbose_name='Link', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='title_en',
            field=models.CharField(max_length=128, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='event',
            name='title_es',
            field=models.CharField(max_length=128, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='event',
            name='title_pt_br',
            field=models.CharField(max_length=128, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='tipforcycling',
            name='content_en',
            field=models.TextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='tipforcycling',
            name='content_es',
            field=models.TextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='tipforcycling',
            name='content_pt_br',
            field=models.TextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='tipforcycling',
            name='title_en',
            field=models.CharField(max_length=128, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='tipforcycling',
            name='title_es',
            field=models.CharField(max_length=128, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='tipforcycling',
            name='title_pt_br',
            field=models.CharField(max_length=128, null=True, verbose_name='Title'),
        ),
    ]
