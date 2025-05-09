from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from datetime import date
from django.utils.timezone import now
from django.apps import apps

from .constants import (
    ROLES_CHOICES,
    STATUS_CHOICES,
    WEAPON_CHOICES,
    GENDER_CHOICES,
    HANDEDNESS_CHOICES,
    STATUS_BADGES,
)


class Member(models.Model):
    """Represents a fencing association member."""

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be in format: '+999999999'.",
    )

    # Personal Information
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    birth_date = models.DateField(
        verbose_name="Birth Date", null=True, blank=True
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name="Phone Number",
    )

    # Address
    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Address"
    )
    address_complement = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Address Complement",
    )
    postal_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Postal Code"
    )
    city = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="City"
    )

    # Relationships & Categorization
    roles = models.CharField(
        max_length=20,
        choices=ROLES_CHOICES,
        default="visitor",
        blank=True,
        verbose_name="Role",
    )
    sports_category = models.ForeignKey(
        "sport.SportsCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sports Category",
    )

    # Status & Dates
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Status",
    )
    weapon = models.CharField(
        max_length=10,
        choices=WEAPON_CHOICES,
        verbose_name="Weapon",
        blank=True,
        null=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name="Gender",
        blank=True,
        null=True,
    )
    handedness = models.CharField(
        max_length=15,
        choices=HANDEDNESS_CHOICES,
        verbose_name="Handedness",
        blank=True,
        null=True,
    )

    date_joined = models.DateField(
        auto_now_add=True, verbose_name="Date Joined"
    )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name="Last Updated"
    )

    # Media
    photo = models.ImageField(
        upload_to="member_photos/", blank=True, null=True, verbose_name="Photo"
    )

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Member"
        verbose_name_plural = "Members"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_photo_url(self):
        """Returns the member's photo URL if available."""
        return self.photo.url if self.photo else None

    def get_age(self):
        """Returns the age of the member based on birth_date."""
        if not self.birth_date:
            return None
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - (
                (today.month, today.day)
                < (self.birth_date.month, self.birth_date.day)
            )
        )

    def get_status_badge(self):
        """Returns the CSS class for the status badge."""
        return STATUS_BADGES.get(self.status, "badge-secondary")

    def assign_sports_category(self):
        """Automatically assigns the correct sports category based on the member's age."""
        if not self.birth_date:
            return None

        birth_year = self.birth_date.year
        SportsCategory = apps.get_model("sport", "SportsCategory")

        # Récupération des catégories via le cache
        categories = cache.get("sports_categories")
        if not categories:
            categories = list(SportsCategory.objects.all())
            cache.set("sports_categories", categories, 3600)

        # Attribution de la catégorie
        for category in categories:
            if category.is_applicable(birth_year):
                self.sports_category = category
                self.save(update_fields=["sports_category"])
                return category
        return None

    def clean(self):
        """Validation centralisée."""
        if self.birth_date and self.birth_date > date.today():
            raise ValidationError(
                "La date de naissance ne peut pas être dans le futur."
            )

        # Vérifier si un email similaire existe (sans tenir compte de la casse)
        if (
            Member.objects.filter(email__iexact=self.email)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError("Cet email est déjà utilisé.")

    def save(self, *args, **kwargs):
        """Nettoyage avant sauvegarde."""
        if kwargs.get("update_fields") is None:
            self.full_clean()
        super().save(*args, **kwargs)

    def create_payment(self):
        """Crée un paiement basé sur la catégorie sportive."""
        if not self.sports_category:
            raise ValidationError("Le membre n'a pas de catégorie assignée.")
        MembershipFee.objects.create(
            member=self,
            sports_category=self.sports_category,
            amount=self.sports_category.fee_amount,
            payment_date=now().date(),
            is_valid=True,
        )


class MembershipFee(models.Model):
    """Tracks membership fee payments for members."""

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="fees"
    )
    sports_category = models.ForeignKey(
        "sport.SportsCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Category",
        help_text="Catégorie associée à ce paiement",
    )
    is_valid = models.BooleanField(default=False, verbose_name="Valid Payment")

    class Meta:
        ordering = ["member"]

    def __str__(self):
        status = "Valid" if self.is_valid else "Unpaid"
        return f"{self.member} - {status} €"
