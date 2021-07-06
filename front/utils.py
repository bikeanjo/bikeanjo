import re
from django.utils.timezone import datetime
from bikeanjo import settings
from cyclists.models import User

DATE_RE = re.compile(r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$')


class DateParser(object):
    def __init__(self, **kwargs):
        self.date_re = kwargs.get('date_re', DATE_RE)

    def parse_date(self, strdate):
        match = self.date_re.match(strdate)
        if not match:
            return

        params = {}
        for p, v in list(match.groupdict().items()):
            params[p] = int(v)

        return datetime(**params)


def set_language(recipient):
    if not isinstance(recipient, User):
        user = User.objects.get(email=recipient)
    else:
        user = recipient
    return user.language or settings.LANGUAGE_CODE
