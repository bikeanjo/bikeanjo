# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.utils.text import slugify


def populate_slug_field(apps, schema):
    Event = apps.get_model("front", "Event")

    for event in Event.objects.all():
        event.slug = slugify(event.title)
        event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0002_point_helprequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(default='', verbose_name='Slug', max_length=128, editable=False),
            preserve_default=False,
        ),
        migrations.RunPython(populate_slug_field),
    ]
