# -*- coding: utf-8 -*-


from django.db import models, migrations


def migrate_city_data_on_event(apps, schema_editor):
    Event = apps.get_model('front', 'Event')
    City = apps.get_model('cities', 'City')

    names = set(Event.objects.values_list('v1_city', flat=True).distinct())
    for name in names:
        city = City.objects.filter(name=name.strip()).first()
        if city:
            Event.objects.filter(v1_city=name).update(city=city)



class Migration(migrations.Migration):

    dependencies = [
        ('front', '0039_auto_20160401_1039'),
    ]

    operations = [
        migrations.RunPython(migrate_city_data_on_event)
    ]
