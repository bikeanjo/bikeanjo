# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import select_template

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
    subject = u'Seu pedido #%d foi cancelado por %s!' % (helprequest.id, bikeanjo.first_name)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.requester

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


# forms.HelpRequestUpdateForm
def notify_that_bikeanjo_cannot_help_anymore(helprequest, bikeanjo):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    subject = 'Seu pedido #%d foi cancelado por %s!' % (helprequest.id, bikeanjo.first_name)
    from_email = settings.DEFAULT_FROM_EMAIL
    helprequest = helprequest
    recipient = helprequest.requester

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


# management/commands/review_matches.py
def notify_cant_find_bikeanjo(helprequest):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    subject = 'Ainda não achamos seu bike anjo, mas queremos te ajudar!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.requester

    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'site': site,
    }

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
    subject = u'Você recebeu uma nova mensagem de %s!' % reply.author.get_full_name()
    from_email = settings.DEFAULT_FROM_EMAIL
    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'sender': reply.author,
        'site': site,
    }

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
    subject = 'O Bike Anjo achou alguém para te ajudar com o pedido #%d!' % helprequest.id
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.requester

    data = {
        'helprequest': helprequest,
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
    subject = 'Você recebeu um pedido #%d de ajuda!' % helprequest.id
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


# forms.HelpRequestUpdateForm
def notify_requester_about_attended_request(helprequest):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    subject = u'Seu pedido #%d de Bike Anjo foi atendido por %s?' % (helprequest.id, helprequest.bikeanjo.get_full_name())
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.requester

    data = {
        'helprequest': helprequest,
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


# views.HomeView
def notify_user_subscribed_in_newsletter(subscriber):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    subject = 'Você se inscreveu para o boletim do Bikeanjo!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = subscriber

    data = {
        'site': site,
        'subscriber': subscriber,
    }

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
    subject = u'Feedback de %s' % feedback.author.get_full_name()
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
