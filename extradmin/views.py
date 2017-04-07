# -*- coding: utf-8 -*-
from django.db.models.aggregates import Avg, Count
from django.views.generic import TemplateView

from cyclists.models import Bikeanjo
from front.models import HelpRequest

HELP_OPTIONS = HelpRequest.HELP_OPTIONS


class SummaryAdminView(TemplateView):
    template_name = 'admin/summary.html'

    def get_context_data(self, **kwargs):
        data = super(SummaryAdminView, self).get_context_data(**kwargs)
        bikeanjos = Bikeanjo.objects.filter(accepted_agreement=True)
        requests = HelpRequest.objects.filter(requester__accepted_agreement=True)
        feedback_avg = requests\
            .filter(requester_rating__gt=0)\
            .aggregate(Avg('requester_rating'))\
            .get('requester_rating__avg')

        requests_attended = requests.filter(status='attended')
        requests_failed = requests.filter(status__in=['canceled', 'rejected'])
        requests_active = requests.exclude(bikeanjo=None).filter(status__in=['new', 'open'])
        requests_canceled_ba = requests.filter(status='canceled', closed_by='bikeanjo')
        requests_canceled_req = requests.filter(status='canceled', closed_by='requester')
        requests_abandoned = requests.filter(status='new', bikeanjo=None)

        total = requests.count()
        totals_by_type = requests.values_list('help_with').annotate(total=Count(1))
        totals_by_type = [(100 * total_type / total, HELP_OPTIONS.get(type_id)) for type_id, total_type in totals_by_type]

        data['bikeanjos'] = bikeanjos
        data['requests'] = requests
        data['feedback_avg'] = feedback_avg
        data['requests_attended'] = requests_attended
        data['requests_failed'] = requests_failed
        data['requests_active'] = requests_active
        data['requests_canceled_ba'] = requests_canceled_ba
        data['requests_canceled_req'] = requests_canceled_req
        data['requests_abandoned'] = requests_abandoned
        data['totals_by_type'] = totals_by_type

        return data