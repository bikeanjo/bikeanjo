import re
from django.utils.timezone import datetime

DATE_RE = re.compile(r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$')


class DateParser(object):
    def __init__(self, **kwargs):
        self.date_re = kwargs.get('date_re', DATE_RE)

    def parse_date(self, strdate):
        match = self.date_re.match(strdate)
        if not match:
            return

        params = {}
        for p, v in match.groupdict().items():
            params[p] = int(v)

        return datetime(**params)
