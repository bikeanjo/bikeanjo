# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import select_template
from django.utils.timezone import now
from front import models

# {'update_fields': None,
# 'instance': <HelpRequest: HelpRequest object>,
# 'signal': <django.db.models.signals.ModelSignal object at 0x7fedc3339e50>,
# 'created': False, 'raw': False, 'using': 'default'}


@receiver(post_save, sender=models.HelpRequest)
def assign_bike_anjo(sender, instance, **kwargs):
    if instance.bikeanjo is None:
        result = instance.find_bikeanjo()

        if not (result and len(result) == 3):
            return

        score, track, bikeanjo = result
        instance.bikeanjo = bikeanjo
        instance.save()

        old_match = models.Match.objects.filter(helprequest=instance)
        if old_match.exists():
            old_match = old_match.latest('id')
            old_match.rejected_date = now()
            old_match.save()

        models.Match.objects.create(
            bikeanjo=bikeanjo,
            helprequest=instance,
            score=score,
        )


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
    subject = 'Você recebeu uma nova mensagem'
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
