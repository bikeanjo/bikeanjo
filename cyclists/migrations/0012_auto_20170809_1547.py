# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyclists', '0011_auto_20160607_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(default=b'pt-br', max_length=8, verbose_name='Language', choices=[(b'pt-br', 'Brazilian Portuguese'), (b'es', 'Spanish'), (b'en', 'English'), (b'fr', 'French')]),
        ),
    ]
