# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import select_template
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from front.utils import set_language

logger = logging.getLogger('front.notifications')

__all__ = (
    'notify_that_bikeanjo_canceled_request_by_inactivity',
    'notify_that_bikeanjo_cannot_help_anymore',
    'notify_cant_find_bikeanjo',
    'notify_new_reply_by_email',
    'notify_requester_about_found_bikeanjo',
    'notify_bikeanjo_about_new_request',
    'notify_requester_about_attended_request',
    'notify_user_subscribed_in_newsletter',
    'notify_admins_about_new_contact_message',
)


# forms.HelpRequestUpdateForm
def notify_that_bikeanjo_canceled_request_by_inactivity(helprequest, bikeanjo):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.requester

    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'site': site,
    }

    with translation.override(set_language(recipient)):
        subject = _('Your request #%(id)d was cancelled by %(ba)s!') % {'id': helprequest.id, 'ba': bikeanjo.first_name}

        template_name = 'emails/request_canceled_by_inactivity.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/request_canceled_by_inactivity.txt'
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


# forms.HelpRequestUpdateForm
def notify_that_bikeanjo_cannot_help_anymore(helprequest, bikeanjo):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    from_email = settings.DEFAULT_FROM_EMAIL
    helprequest = helprequest
    recipient = helprequest.requester

    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'site': site,
    }

    with translation.override(set_language(recipient)):
        subject = _('Your request #%(id)d was cancelled by %(ba)s!') % {'id': helprequest.id, 'ba': bikeanjo.first_name}

        template_name = 'emails/request_canceled_by_bikeanjo.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/request_canceled_by_bikeanjo.txt'
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


# management/commands/review_matches.py
# TODO: send this email for requests without bikeanjo 
def notify_cant_find_bikeanjo(helprequest):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.requester

    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'site': site,
    }

    with translation.override(set_language(recipient)):
        subject = _('We can\'t find a bike anjo yet, but we want to help you!')

        template_name = 'emails/cant_find_bikeanjo.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/cant_find_bikeanjo.txt'
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


# forms.RequestReplyForm
def notify_new_reply_by_email(reply):
    helprequest = reply.helprequest

    recipient = None
    if reply.author != helprequest.requester:
        recipient = helprequest.requester
    elif helprequest.bikeanjo:
        recipient = helprequest.bikeanjo

    if not recipient:
        return

    site = Site.objects.filter(id=settings.SITE_ID).first()
    from_email = settings.DEFAULT_FROM_EMAIL
    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'sender': reply.author,
        'site': site,
    }

    with translation.override(set_language(recipient)):
        subject = _('You have a new message from %(user)s!') % {'user': reply.author.get_full_name()}

        template_name = 'emails/new_msg_to_%s.html' % recipient.role
        html = select_template([template_name]).render(data)

        template_name = 'emails/new_msg_to_%s.txt' % recipient.role
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


# forms.BikeanjoAcceptRequestForm
def notify_requester_about_found_bikeanjo(helprequest):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.requester

    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'site': site,
    }

    with translation.override(set_language(recipient)):
        subject = _('Bike Anjo found someone to help you on your request #%(id)d!') % {'id': helprequest.id}

        template_name = 'emails/found_bikeanjo.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/found_bikeanjo.txt'
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


# forms.HelpRequestCompleteForm
def notify_bikeanjo_about_new_request(helprequest):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.bikeanjo

    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'site': site,
    }

    with translation.override(set_language(recipient)):
        subject = _('You have a new request for help #%(id)d!') % {'id': helprequest.id}

        template_name = 'emails/new_request.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/new_request.txt'
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


# forms.HelpRequestUpdateForm
def notify_requester_about_attended_request(helprequest):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.requester

    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'site': site,
    }

    with translation.override(set_language(recipient)):
        subject = _('Was you request #%(id)d at Bike Anjo attended by %(ba)s?') % {'id': helprequest.id, 'ba': helprequest.bikeanjo.get_full_name()}

        template_name = 'emails/request_attended.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/request_attended.txt'
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


# views.HomeView
def notify_user_subscribed_in_newsletter(subscriber):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = subscriber

    data = {
        'site': site,
        'subscriber': subscriber,
    }

    subject = _('You subscribed to Bike Anjo mailing news!')

    template_name = 'emails/newsletter_subscription.txt'
    text = select_template([template_name]).render(data)

    msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
    msg.send()


# views.ContactView
def notify_admins_about_new_contact_message(contact):
    from_email = contact.email
    recipient = settings.DEFAULT_TO_EMAIL
    subject = contact.subject
    content = 'From "%s<%s>, %s' % (
        contact.name,
        contact.email,
        contact.created_date.strftime('%d/%m/%Y %H:%M'),
    )
    content += '\n%s\n\n' % ('-' * len(content))
    content += contact.message

    msg = EmailMultiAlternatives(subject, content, from_email, [recipient],
                                 reply_to=[from_email])
    msg.send()


# views.ContactView
def notify_admins_about_new_feedback(feedback):
    from_email = feedback.author.email
    recipient = settings.DEFAULT_TO_EMAIL
    subject = _('Feedback from %s') % {'user': feedback.author.get_full_name()}
    content = u'From "%s<%s>, %s' % (
        feedback.author.get_full_name(),
        feedback.author.email,
        feedback.created_date.strftime('%d/%m/%Y %H:%M'),
    )
    content += '\n%s\n\n' % ('-' * len(content))
    content += feedback.message

    msg = EmailMultiAlternatives(subject, content, from_email, [recipient],
                                 reply_to=[from_email])
    msg.send()
