# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cyclists.models


class Migration(migrations.Migration):

    dependencies = [
        ('cyclists', '0002_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to=cyclists.models.get_upload_path, storage=cyclists.models.AvatarStorage(), verbose_name='Avatar', blank=True),
        ),
    ]
