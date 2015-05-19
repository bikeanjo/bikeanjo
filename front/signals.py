# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
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
