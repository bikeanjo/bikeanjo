# -*- coding: utf-8 -*-


from django.db import models, migrations
import slider.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlideItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Date of change')),
                ('active', models.BooleanField(default=False, verbose_name='Valid')),
                ('image', models.ImageField(upload_to=b'slides', verbose_name='Image')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('site', models.ForeignKey(default=slider.models.default_to_first_site, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Slide',
                'verbose_name_plural': 'Slides',
            },
        ),
    ]
