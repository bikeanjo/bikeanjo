# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyclists', '0005_auto_20150831_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(default=b'pt-br', max_length=8, choices=[(b'pt-br', 'Brazilian Portuguese'), (b'es', 'Spanish'), (b'en', 'English')]),
        ),
    ]
