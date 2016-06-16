# -*- coding: utf-8 -*-
from import_export import resources
from cyclists.models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'date_joined', 'last_login',
                  'gender', 'birthday', 'role', 'help_with', 'available', 'city', 'country', 'accepted_agreement',)
        export_order = ('first_name', 'last_name', 'email', 'date_joined', 'last_login',
                        'gender', 'birthday', 'role', 'help_with', 'available', 'city', 'country', 'accepted_agreement',)

    def dehydrate_help_with(self, obj):
        if obj.role == 'requester':
            return ''
        return ' / '.join([str(label) for label in obj.help_labels()])

    def dehydrate_city(self, obj):
        if obj.city and obj.city.name:
            return obj.city.name
        return '*' + obj.v1_city

    def dehydrate_country(self, obj):
        if obj.country and obj.country.name:
            return obj.country.name
        return '*' + obj.v1_country
