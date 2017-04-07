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
        totals_by_type = {}

        for res in requests.values('help_with', 'status').annotate(total=Count(1)):
            label = HELP_OPTIONS.get(res['help_with'])
            status = res['status']

            if label not in totals_by_type:
                totals_by_type[label] = {}
            if status not in totals_by_type[label]:
                totals_by_type[label][status] = {}
            if 'all' not in totals_by_type[label]:
                totals_by_type[label]['all'] = {'absolute': 0, 'perc': 0}
            current = totals_by_type[label]['all']

            totals_by_type[label][status] = {
                'absolute': res['total'],
                'perc': 100 * res['total'] / total
            }
            totals_by_type[label]['all'] = {
                'absolute': current['absolute'] + res['total'],
                'perc': 100 * (current['absolute'] + res['total']) / total
            }

        total = requests.filter(requester_rating__gt=0).count()
        totals_by_rating = [0, 0, 0, 0, 0]

        results = requests\
            .filter(requester_rating__gt=0, requester_rating__lt=6)\
            .values('requester_rating')\
            .annotate(total=Count(1))

        for res in results:
            rating = res['requester_rating'] - 1
            totals_by_rating[rating] = {
                'absolute': res['total'],
                'perc': 100 * res['total'] / total
            }

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
        data['totals_by_rating'] = totals_by_rating

        return data