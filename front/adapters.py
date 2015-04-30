import re
from django.utils import timezone
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from utils import DateParser
from front import models

FACEBOOK_DATE_PATTERN = re.compile(r'^(?P<month>\d\d?)/(?P<day>\d\d?)/(?P<year>\d\d\d\d)$')
FACEBOOK_LOCATION_PATTERN = re.compile(r'^(?P<city>[^,]+), *(?P<country>.*)$')

FACEBOOK_DATE_PARSER = DateParser(date_re=FACEBOOK_DATE_PATTERN)


class BikeanjoSocialAccountAdapter(DefaultSocialAccountAdapter):

    def __populate_with_facebook(self, sociallogin, user):
        extra = sociallogin.account.extra_data

        location = extra.get('location', {}).get('name', '')
        match = FACEBOOK_LOCATION_PATTERN.match(location)

        if match:
            user.city = match.groupdict().get('city', '')
            user.country = match.groupdict().get('country', )
        return user

    def populate_user(self, request, sociallogin, data):
        '''
        This is a User instance candidate for Social Signup page
        '''
        user = super(BikeanjoSocialAccountAdapter, self).populate_user(request, sociallogin, data)
        self.__populate_with_facebook(sociallogin, user)
        return user

    def save_user(self, request, sociallogin, form=None):
        extra = sociallogin.account.extra_data
        user = sociallogin.user

        user.birthday = FACEBOOK_DATE_PARSER.parse_date(extra.get('birthday', ''))
        user.gender = extra.get('gender', '')
        user.role = request.session.pop('user_role')

        return super(BikeanjoSocialAccountAdapter, self).save_user(request, sociallogin, form=form)
