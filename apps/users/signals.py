from django.db.models.signals import post_save, pre_save
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from .models import Profile


class UserSignals:
    """
    Class managing Django user-related signals.
    This class contains callback methods for pre_save and post_save signals
    of the User model.
    """

    @classmethod
    def post_save(cls, sender, instance, created, **kwargs):
        """
        Signal executed after a user is saved.

        Creates a user profile when a new user is created.
        Also handles primary email synchronization with django-allauth.

        Args:
            sender: The model sending the signal (User)
            instance: The user instance that was just saved
            created (bool): True if the user was just created, False otherwise
            **kwargs: Additional signal arguments
        """
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
        """
        Signal executed before a user is saved.

        Converts the username to lowercase before saving.

        Args:
            sender: The model sending the signal (User)
            instance: The user instance about to be saved
            **kwargs: Additional signal arguments
        """
        if instance.username:
            instance.username = instance.username.lower()


# Signal connections
post_save.connect(UserSignals.post_save, sender=User)
pre_save.connect(UserSignals.pre_save, sender=User)
