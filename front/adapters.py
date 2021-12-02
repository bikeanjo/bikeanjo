# -*- coding: utf-8 -*-
import re
from django.conf.urls import reverse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import perform_login
from .utils import DateParser
from cyclists.models import User

from cities.models import Country, CityAlias

FACEBOOK_DATE_PATTERN = re.compile(
    r'^(?P<month>\d\d?)/(?P<day>\d\d?)/(?P<year>\d\d\d\d)$')
FACEBOOK_LOCATION_PATTERN = re.compile(r'^(?P<city>[^,]+), *(?P<country>.*)$')

FACEBOOK_DATE_PARSER = DateParser(date_re=FACEBOOK_DATE_PATTERN)


class BikeanjoAccountAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):
        # wrapper for django.contrib.messages.add_message
        pass


class BikeanjoSocialAccountAdapter(DefaultSocialAccountAdapter):

    def __assign_location_to_user(self, location, user):
        country = location.get('country', '')
        city = location.get('city', '')

        user.country = Country.objects.filter(name=country).first()
        user.city_alias = CityAlias.objects.filter(
            name__lowermatch=city).first()

        if user.city_alias:
            user.city = user.city_alias.city
            if not user.country:
                user.country = user.city.country
        return user

    def __populate_with_facebook(self, sociallogin, user):
        extra = sociallogin.account.extra_data
        location = extra.get('location', {}).get('name', '')
        match = FACEBOOK_LOCATION_PATTERN.match(location)
        if match:
            user = self.__assign_location_to_user(match.groupdict(), user)
        return user

    def __populate_with_twitter(self, sociallogin, user):
        extra = sociallogin.account.extra_data
        location = extra.get('location', '')
        match = FACEBOOK_LOCATION_PATTERN.match(location)
        if match:
            user = self.__assign_location_to_user(match.groupdict(), user)
        return user

    def populate_user(self, request, sociallogin, data):
        '''
        This is a User instance candidate for Social Signup page
        '''
        user = super(BikeanjoSocialAccountAdapter, self).populate_user(
            request, sociallogin, data)

        populator = {
            'twitter': self.__populate_with_twitter,
            'facebook': self.__populate_with_facebook,
        }.get(sociallogin.account.provider, lambda l, u: u)

        return populator(sociallogin, user)

    def save_user(self, request, sociallogin, form=None):
        extra = sociallogin.account.extra_data
        user = sociallogin.user

        user.birthday = FACEBOOK_DATE_PARSER.parse_date(
            extra.get('birthday', ''))
        user.gender = extra.get('gender', '')
        user.role = request.session.pop('user_role')

        return super(BikeanjoSocialAccountAdapter, self).save_user(request, sociallogin, form=form)

    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):
        # wrapper for django.contrib.messages.add_message
        pass

    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user

        if user.id or not user.email:
            return
        try:
            user = User.objects.get(email=user.email)
            sociallogin.state['next'] = reverse('cyclist_dashboard')
            sociallogin.state['process'] = 'connect'
            perform_login(request, user, 'none')
        except User.DoesNotExist:
            if 'user_role' not in request.session:
                sociallogin.state['next'] = reverse('signup_define_role')
                sociallogin.state['process'] = 'redirect'
