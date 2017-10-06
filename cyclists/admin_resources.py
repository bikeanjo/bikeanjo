# -*- coding: utf-8 -*-
from import_export import fields
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


# - Cidade;
# ⚡ Estado?
# - País;
# - Gênero;
# - Idade;
# - Há quanto tempo pedala;
# - Frequência de uso da bicicleta como meio de transporte (pergunta "Você usa a bike como meio de transporte?");
# - Iniciativas de bicicleta (pergunta "Participa de alguma iniciativa de bicicleta?)
# - Como você pode ajudar (ajudar a pedalar, sugerir rotas etc.).
# ⚡ Número de pedidos (novos, abertos, atendidos, finalizados, cancelados, rejeitados);
# ⚡ Número de rotas ou pontos informados.

class BikeanjoResource(UserResource):
    requests_total = fields.Field()
    requests_new = fields.Field()
    requests_open = fields.Field()
    requests_attended = fields.Field()
    requests_finished = fields.Field()
    requests_canceled = fields.Field()
    requests_rejected = fields.Field()
    routes_count = fields.Field()
    points_count = fields.Field()
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'date_joined',
            'last_login',
            'city',
            'country',
            'gender',
            'birthday',
            'ride_experience',
            'bike_use',
            'initiatives',
            'help_with',
            'available',
            'accepted_agreement',
            'requests_total',
            'requests_new',
            'requests_open',
            'requests_attended',
            'requests_finished',
            'requests_canceled',
            'requests_rejected',
            'routes_count',
            'points_count',
        )
        export_order = (
            'first_name',
            'last_name',
            'email',
            'date_joined',
            'last_login',
            'city',
            'country',
            'gender',
            'birthday',
            'ride_experience',
            'bike_use',
            'initiatives',
            'help_with',
            'available',
            'accepted_agreement',
            'requests_total',
            'requests_new',
            'requests_open',
            'requests_attended',
            'requests_finished',
            'requests_canceled',
            'requests_rejected',
            'routes_count',
            'points_count',
        )

    def get_queryset(self):
        queryset = super(BikeanjoResource, self).get_queryset()
        return queryset.filter(role='bikeanjo')

    def dehydrate_requests_total(self, ba):
        return ba.helpbikeanjo_set.count()

    def dehydrate_requests_new(self, ba):
        return ba.helpbikeanjo_set.filter(status='new').count()

    def dehydrate_requests_open(self, ba):
        return ba.helpbikeanjo_set.filter(status='open').count()

    def dehydrate_requests_attended(self, ba):
        return ba.helpbikeanjo_set.filter(status='attended').count()

    def dehydrate_requests_finalized(self, ba):
        return ba.helpbikeanjo_set.filter(status='finalized').count()

    def dehydrate_requests_canceled(self, ba):
        return ba.helpbikeanjo_set.filter(status='canceled').count()

    def dehydrate_requests_rejected(self, ba):
        return ba.helpbikeanjo_set.filter(status='rejected').count()

    def dehydrate_requests_eba(self, ba):
        return ba.helpbikeanjo_set.filter(status='eba').count()

    def dehydrate_routes_count(self, ba):
        return ba.track_set.count()

    def dehydrate_points_count(self, ba):
        return ba.point_set.count()


# Cidade;
# Estado?
# País;
# Gênero;
# Idade;
# Experiência com a bicicleta;
# Número de pedidos (novos, abertos, atendidos, finalizados, cancelados, rejeitados);
# Tipo de pedido (aprender a pedalar, praticar pedaladas, acompanhamento no trânsito etc.).
class RequesterResource(UserResource):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'date_joined',
            'last_login',
            'city',
            'country',
            'gender',
            'birthday',
            'ride_experience',
            'accepted_agreement',
        )
        export_order = (
            'first_name',
            'last_name',
            'email',
            'date_joined',
            'last_login',
            'city',
            'country',
            'gender',
            'birthday',
            'ride_experience',
            'accepted_agreement',
        )

    def get_queryset(self):
        queryset = super(RequesterResource, self).get_queryset()
        return queryset.filter(role='requester')
