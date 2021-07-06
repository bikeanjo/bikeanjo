# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0018_countryalias_name_index'),
        ('front', '0038_auto_20160401_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.ForeignKey(to='cities.City', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='v1_city',
            field=models.CharField(verbose_name='City', max_length=b'64', editable=False, blank=True),
        ),
    ]
