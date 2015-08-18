# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import select_template

from fieldsignals import post_save_changed

from front import models
from cyclists.models import User

logger = logging.getLogger('front.notifications')

__all__ = (
    'notify_that_bikeanjo_canceled_request_by_inactivity',
    'notify_that_bikeanjo_cannot_help_anymore',
    'notify_that_bikeanjo_rejected_new_request',
    'notify_new_reply_by_email',
    'notify_requester_about_found_bikeanjo',
    'notify_bikeanjo_about_new_request',
    'notify_requester_about_attended_request',
    'notify_user_subscribed_in_newsletter',
    'notify_admins_about_new_contact_message',
)


def notify_that_bikeanjo_canceled_request_by_inactivity(sender, instance, changed_fields, **kwargs):
    remap = dict([field.name, {'old': value[0], 'new': value[1]}] for field, value in changed_fields.items())
    status = remap.get('status', {})

    if 'bikeanjo' in remap:
        bikeanjo_id = remap.get('bikeanjo', {}).get('old')
        bikeanjo = User.objects.filter(id=bikeanjo_id).first()

    if status.get('old') == 'open' and status.get('new') == 'canceled' and instance.closed_by == 'bikeanjo':
        site = Site.objects.filter(id=settings.SITE_ID).first()
        subject = 'Seu pedido de bike anjo foi cancelado por %s!' % bikeanjo.first_name
        from_email = settings.DEFAULT_FROM_EMAIL
        helprequest = instance
        recipient = instance.requester

        data = {
            'helprequest': helprequest,
            'recipient': recipient,
            'site': site,
        }

        template_name = 'emails/request_canceled_by_inactivity.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/request_canceled_by_inactivity.txt'
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


def notify_that_bikeanjo_cannot_help_anymore(sender, instance, changed_fields, **kwargs):
    remap = dict([field.name, {'old': value[0], 'new': value[1]}] for field, value in changed_fields.items())
    status = remap.get('status', {})

    if 'bikeanjo' in remap:
        bikeanjo_id = remap.get('bikeanjo', {}).get('old')
        bikeanjo = User.objects.filter(id=bikeanjo_id).first()

    if status.get('old') == 'open' and status.get('new') == 'new' and instance.closed_by == 'bikeanjo':
        site = Site.objects.filter(id=settings.SITE_ID).first()
        subject = 'Seu pedido de bike anjo foi cancelado por %s!' % bikeanjo.first_name
        from_email = settings.DEFAULT_FROM_EMAIL
        helprequest = instance
        recipient = instance.requester

        data = {
            'helprequest': helprequest,
            'recipient': recipient,
            'site': site,
        }

        template_name = 'emails/request_canceled_by_bikeanjo.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/request_canceled_by_bikeanjo.txt'
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


def notify_that_bikeanjo_rejected_new_request(sender, instance, changed_fields, **kwargs):
    field_names = [field.name for field in changed_fields.keys()]

    # se o pedido é novo e a única alteração é o bikeanjo
    if (instance.status == 'new') and ('bikeanjo' in field_names) and len(field_names) == 1:
        site = Site.objects.filter(id=settings.SITE_ID).first()
        subject = 'O Bikeanjo teve um problema!'
        from_email = settings.DEFAULT_FROM_EMAIL
        helprequest = instance
        recipient = instance.requester

        data = {
            'helprequest': helprequest,
            'recipient': recipient,
            'site': site,
        }

        template_name = 'emails/request_rejected_by_bikeanjo.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/request_rejected_by_bikeanjo.txt'
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


def notify_new_reply_by_email(sender, instance, **kwargs):
    helprequest = instance.helprequest

    recipient = None
    if instance.author != helprequest.requester:
        recipient = helprequest.requester
    elif helprequest.bikeanjo:
        recipient = helprequest.bikeanjo

    if not recipient:
        return

    site = Site.objects.filter(id=settings.SITE_ID).first()
    subject = 'Você recebeu uma nova mensagem!'
    from_email = settings.DEFAULT_FROM_EMAIL
    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'sender': instance.author,
        'site': site,
    }

    template_name = 'emails/new_msg_to_%s.html' % recipient.role
    html = select_template([template_name]).render(data)

    template_name = 'emails/new_msg_to_%s.txt' % recipient.role
    text = select_template([template_name]).render(data)

    msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
    msg.attach_alternative(html, "text/html")
    msg.send()


def notify_requester_about_found_bikeanjo(sender, instance, changed_fields, **kwargs):
    old_val, new_val = changed_fields.values()[0]

    if old_val != new_val and new_val == 'open':
        site = Site.objects.filter(id=settings.SITE_ID).first()
        subject = 'Achamos um bikeanjo para seu pedido!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient = instance.requester

        data = {
            'helprequest': instance,
            'recipient': recipient,
            'site': site,
        }

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
    subject = 'Você recebeu um pedido de ajuda!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.bikeanjo

    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'site': site,
    }

    template_name = 'emails/new_request.html'
    html = select_template([template_name]).render(data)

    template_name = 'emails/new_request.txt'
    text = select_template([template_name]).render(data)

    msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
    msg.attach_alternative(html, "text/html")
    msg.send()


def notify_requester_about_attended_request(sender, instance, changed_fields, **kwargs):
    old_val, new_val = changed_fields.values()[0]

    if old_val != new_val and new_val == 'attended':
        site = Site.objects.filter(id=settings.SITE_ID).first()
        subject = 'O BikeAnjo marcou seu pedido como atendido!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient = instance.requester

        data = {
            'helprequest': instance,
            'recipient': recipient,
            'site': site,
        }

        template_name = 'emails/request_attended.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/request_attended.txt'
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


def notify_user_subscribed_in_newsletter(sender, instance, created, **kwargs):
    if created:
        site = Site.objects.filter(id=settings.SITE_ID).first()
        subject = 'Você se inscreveu para o boletim do Bikeanjo!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient = instance

        data = {
            'site': site,
            'subscriber': instance,
        }

        template_name = 'emails/newsletter_subscription.txt'
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.send()


def notify_admins_about_new_contact_message(sender, instance, created, **kwargs):
        if not created:
            return

        from_email = instance.email
        recipient = settings.DEFAULT_FROM_EMAIL
        subject = instance.subject
        content = 'From "%s<%s>, %s' % (
            instance.name,
            instance.email,
            instance.created_date.strftime('%d/%m/%Y %H:%M'),
        )
        content += '\n%s\n\n' % ('-' * len(content))
        content += instance.message

        msg = EmailMultiAlternatives(subject, content, from_email, [recipient],
                                     reply_to=[from_email])
        msg.send()
