# -*- coding: utf-8 -*-
from import_export import resources
from cyclists.models import User
from front import models


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'role', 'city', 'country',)


class NewsletterResource(resources.ModelResource):
    class Meta:
        model = models.Subscriber
        fields = ('created_date', 'email', 'valid',)
