# -*- coding: utf-8 -*-


from django.db import migrations
from django.db.migrations.operations.base import Operation


class LoadExtension(Operation):

    reversible = True

    def __init__(self, name):
        self.name = name

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute("CREATE EXTENSION IF NOT EXISTS %s" % self.name)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute("DROP EXTENSION %s" % self.name)

    def describe(self):
        return "Creates extension %s" % self.name


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0012_load_cities_from_world'),
    ]

    operations = [
        LoadExtension('fuzzystrmatch'),
    ]
