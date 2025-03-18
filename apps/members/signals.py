from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member


@receiver(post_save, sender=Member)
def auto_assign_category(sender, instance, created, **kwargs):
    if created:
        instance.assign_sports_category()
