# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyclists', '0004_user_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=64, verbose_name='City', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='initiatives',
            field=models.TextField(blank=True),
        ),
    ]
