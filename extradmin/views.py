# -*- coding: utf-8 -*-
from django import forms
from django.db.models.aggregates import Avg, Count
from django.views.generic import TemplateView

from cities.models import City, Country
from cyclists.models import Bikeanjo
from front.models import HelpRequest

HELP_OPTIONS = HelpRequest.HELP_OPTIONS


class SummaryAdminView(TemplateView):
    template_name = 'admin/summary.html'

    def get_context_data(self, **kwargs):
        data = super(SummaryAdminView, self).get_context_data(**kwargs)
        requests = HelpRequest.objects.filter(requester__accepted_agreement=True)
        bikeanjos = Bikeanjo.objects.filter(accepted_agreement=True, is_active=True)

        country = self.request.GET.get('country', '')
        if country.isdigit():
            country = Country.objects.get(id=country)
            requests = requests.filter(requester__country=country)
            bikeanjos = bikeanjos.filter(country=country)

        city = self.request.GET.get('city', '')
        if city.isdigit():
            city = City.objects.get(id=city)
            requests = requests.filter(requester__city=city)
            bikeanjos = bikeanjos.filter(city=city)

        datefield = forms.DateField()
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')

        try:
            start_date = datefield.clean(start_date)
            requests = requests.filter(created_date__gt=start_date)
        except:
            pass

        try:
            end_date = datefield.clean(end_date)
            requests = requests.filter(created_date__lt=end_date)
        except:
            pass

        feedback_avg = requests\
            .filter(requester_rating__gt=0)\
            .aggregate(Avg('requester_rating'))\
            .get('requester_rating__avg')

        requests_attended = requests.filter(status__in=['attended', 'finalized'])
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

        attended_avg = requests_attended.count() / float(max(1, bikeanjos.count()))

        data['attended_avg'] = attended_avg
        data['bikeanjos'] = bikeanjos
        data['city'] = city
        data['country'] = country
        data['end_date'] = end_date
        data['feedback_avg'] = feedback_avg
        data['requests_abandoned'] = requests_abandoned
        data['requests_active'] = requests_active
        data['requests_attended'] = requests_attended
        data['requests_canceled_ba'] = requests_canceled_ba
        data['requests_canceled_req'] = requests_canceled_req
        data['requests_failed'] = requests_failed
        data['requests'] = requests
        data['start_date'] = start_date
        data['totals_by_rating'] = totals_by_rating
        data['totals_by_type'] = totals_by_type

        return data
