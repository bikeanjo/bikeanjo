# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailqueue', '0004_queuedmail_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queuedmail',
            name='sender',
            field=models.EmailField(default=b'Equipe Bike Anjo<noreply@bikeanjo.org>', max_length=254, verbose_name='From'),
        ),
    ]
