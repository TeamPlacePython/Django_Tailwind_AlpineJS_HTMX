from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from datetime import date
from .constants import (
    ROLES_CHOICES,
    STATUS_CHOICES,
    WEAPON_CHOICES,
    GENDER_CHOICES,
    HANDENESS_CHOICES,
    STATUS_BADGES,
)


class Tag(models.Model):
    """Flexible tags assigned to members (e.g., Fencer, Volunteer)."""

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SportsCategory(models.Model):
    """Age category for fencing practice."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Sports categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def is_applicable(self, birth_year):
        """Checks if this category applies based on the member's birth year."""
        if self.start_year and self.end_year:
            return self.start_year <= birth_year <= self.end_year
        return False


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
        verbose_name="Address complement",
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
    tags = models.ManyToManyField(
        Tag, related_name="members", blank=True, verbose_name="tag"
    )
    sports_category = models.ForeignKey(
        SportsCategory,
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
        verbose_name="weapon",
        blank=True,
        null=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name="gender",
    )
    handeness = models.CharField(
        max_length=15,
        choices=HANDENESS_CHOICES,
        verbose_name="handeness",
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
        categories = cache.get("sports_categories")

        if not categories:
            categories = list(SportsCategory.objects.all())
            cache.set(
                "sports_categories", categories, 3600
            )  # Cache for 1 hour

        for category in categories:
            if category.is_applicable(birth_year):
                self.sports_category = category
                self.save(update_fields=["sports_category"])
                return category
        return None

    def clean(self):
        """Validation centralisée."""
        # 1. Date de naissance future
        if self.birth_date and self.birth_date > date.today():
            raise ValidationError(
                "La date de naissance ne peut pas être dans le futur."
            )

    def save(self, *args, **kwargs):
        if kwargs.get("update_fields") is None:
            self.full_clean()
        if not self.roles:
            self.roles = "visitor"
        super().save(*args, **kwargs)


class MembershipFee(models.Model):
    """Tracks membership fee payments for members."""

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="fees"
    )
    amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Amount (€)"
    )
    payment_date = models.DateField(
        auto_now_add=True, verbose_name="Payment Date"
    )
    is_valid = models.BooleanField(default=True, verbose_name="Valid Payment")

    class Meta:
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.member} - {self.amount}€ ({'Valid' if self.is_valid else 'Unpaid'})"
