from django.db.models.signals import post_save, pre_save
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from .models import Profile


class UserSignals:

    @classmethod
    def post_save(cls, sender, instance, created, **kwargs):
        user = instance
        if created:
            Profile.objects.create(
                user=user,
            )
        else:
            try:
                email_address = EmailAddress.objects.get_primary(user)
                if email_address.email != user.email:
                    email_address.email = user.email
                    email_address.verified = False
                    email_address.save()
            except EmailAddress.DoesNotExist:
                # if allauth emailaddress doesn't exist create one
                EmailAddress.objects.create(
                    user=user, email=user.email, primary=True, verified=False
                )

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        if instance.username:
            instance.username = instance.username.lower()


# Signal connections
post_save.connect(UserSignals.post_save, sender=User)
pre_save.connect(UserSignals.pre_save, sender=User)
