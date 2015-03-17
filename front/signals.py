from allauth.account.signals import user_signed_up

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from models import Cyclist


@receiver(post_save, sender=User)
def register_cyclist_signal(signal, sender, instance, created, **kwargs):
    if created:
        return Cyclist.objects.create(user=instance)


# @receiver(user_signed_up)
# def populate_cyclist_info(*argz, **kwargs):
#     import ipdb; ipdb.set_trace()
