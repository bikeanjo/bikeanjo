# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0040_migrate_city_data_on_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='city',
            field=models.ForeignKey(blank=True, to='cities.City', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='content',
            field=models.TextField(verbose_name='Content', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='content_en',
            field=models.TextField(null=True, verbose_name='Content', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='content_es',
            field=models.TextField(null=True, verbose_name='Content', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='content_pt_br',
            field=models.TextField(null=True, verbose_name='Content', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title_en',
            field=models.CharField(max_length=128, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title_es',
            field=models.CharField(max_length=128, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title_pt_br',
            field=models.CharField(max_length=128, null=True, verbose_name='Title', blank=True),
        ),
    ]
