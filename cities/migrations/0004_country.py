# -*- coding: utf-8 -*-


from django.db import models, migrations


def create_first_country(apps, schema_editor):
    Country = apps.get_model("cities", "Country")
    Country.objects.create(id=1, name='Brasil', acronym='BR')


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0003_auto_20150527_1706'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('acronym', models.CharField(max_length=4, verbose_name='Acronym')),
            ],
        ),
        migrations.RunPython(create_first_country),
    ]
