# -*- coding: utf-8 -*-
from django.views.generic import TemplateView


class SummaryAdminView(TemplateView):
    template_name = 'admin/summary.html'
