import re
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from utils import DateParser

FACEBOOK_DATE_PATTERN = re.compile(r'^(?P<month>\d\d?)/(?P<day>\d\d?)/(?P<year>\d\d\d\d)$')
FACEBOOK_LOCATION_PATTERN = re.compile(r'^(?P<city>[^,]+), *(?P<country>.*)$')

FACEBOOK_DATE_PARSER = DateParser(date_re=FACEBOOK_DATE_PATTERN)


class BikeanjoAccountAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):
        # wrapper for django.contrib.messages.add_message
        pass


class BikeanjoSocialAccountAdapter(DefaultSocialAccountAdapter):

    def __populate_with_facebook(self, sociallogin, user):
        extra = sociallogin.account.extra_data

        location = extra.get('location', {}).get('name', '')
        match = FACEBOOK_LOCATION_PATTERN.match(location)

        if match:
            user.city = match.groupdict().get('city', '')
            user.country = match.groupdict().get('country', )
        return user

    def __populate_with_twitter(self, sociallogin, user):
        extra = sociallogin.account.extra_data

        location = extra.get('location', '')
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

        populator = {
            'twitter': self.__populate_with_twitter,
            'facebook': self.__populate_with_facebook,
        }.get(sociallogin.account.provider, lambda l, u: u)

        return populator(sociallogin, user)

    def save_user(self, request, sociallogin, form=None):
        extra = sociallogin.account.extra_data
        user = sociallogin.user

        user.birthday = FACEBOOK_DATE_PARSER.parse_date(extra.get('birthday', ''))
        user.gender = extra.get('gender', '')
        user.role = request.session.pop('user_role')

        return super(BikeanjoSocialAccountAdapter, self).save_user(request, sociallogin, form=form)

    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):
        # wrapper for django.contrib.messages.add_message
        pass
