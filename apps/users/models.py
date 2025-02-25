from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """
    User profile template extending Django’s default User template.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        # help_text=_("User profile photo"),
    )
    displayname = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        # help_text=_("Custom display name"),
    )
    info = models.TextField(
        null=True,
        blank=True,
        # help_text=_("Additional user information"),
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return str(self.user)

    def clean(self):
        """Custom validation for the Profile model."""
        if self.displayname and len(self.displayname.strip()) < 2:
            raise ValidationError(
                {
                    "displayname": _(
                        "The display name must contain at least "
                        "2 characters."
                    )
                }
            )

    @property
    def name(self):
        """Returns the display name or the username."""
        if self.displayname:
            return self.displayname.strip()
        return self.user.username

    @property
    def avatar(self):
        """Returns the avatar URL or the default image."""
        if self.image:
            return self.image.url
        return f"{settings.STATIC_URL}images/avatar.svg"
