# -*- coding: utf-8 -*-
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import select_template
from django.utils.timezone import now

from fieldsignals import post_save_changed

from front import models

logger = logging.getLogger('front.signals')


@receiver(post_save, sender=models.HelpRequest)
def assign_bike_anjo(sender, instance, **kwargs):
    if instance.bikeanjo is None and instance.status == 'new':
        score, track, bikeanjo = instance.find_bikeanjo()

        if not bikeanjo:
            logger.debug("Can't find Bikeanjo to HelpRequest(id=%d)" % (instance.id))
            return

        logger.debug('HelpRequest(id=%d) has a new Bikeanjo(id=%d)' % (instance.id, bikeanjo.id))
        instance.bikeanjo = bikeanjo
        instance.save()

        models.Match.objects.create(
            bikeanjo=bikeanjo,
            helprequest=instance,
            score=score,
        )


@receiver(post_save_changed, fields=['bikeanjo'], sender=models.HelpRequest)
def notify_that_bikeanjo_rejected_request(sender, instance, changed_fields, **kwargs):
    old_val, new_val = changed_fields.values()[0]

    if old_val and new_val is None:
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

        template_name = 'emails/request_canceled_by_bikeanjo.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/request_canceled_by_bikeanjo.txt'
        text = select_template([template_name]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


@receiver(post_save, sender=models.HelpReply)
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


@receiver(post_save_changed, fields=['bikeanjo'], sender=models.HelpRequest)
def notify_requester_about_found_bikeanjo(sender, instance, changed_fields, **kwargs):
    old_val, new_val = changed_fields.values()[0]

    if not old_val and new_val and instance.status == 'new':
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


@receiver(post_save_changed, fields=['bikeanjo'], sender=models.HelpRequest)
def notify_bikeanjo_about_new_request(sender, instance, changed_fields, **kwargs):
    old_val, new_val = changed_fields.values()[0]

    if not old_val and new_val and instance.status == 'new':
        site = Site.objects.filter(id=settings.SITE_ID).first()
        subject = 'Você recebeu um pedido de ajuda!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient = instance.bikeanjo

        data = {
            'helprequest': instance,
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


@receiver(post_save_changed, fields=['status'], sender=models.HelpRequest)
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
