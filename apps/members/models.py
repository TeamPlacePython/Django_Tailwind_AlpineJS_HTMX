from django.db import models
from django.core.validators import RegexValidator


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SportsCategory(models.Model):
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
        """Vérifie si la catégorie est applicable en fonction de l'année de naissance du membre."""
        if self.start_year is not None and self.end_year is not None:
            return self.start_year <= birth_year <= self.end_year
        return False


class Member(models.Model):
    STATUS_CHOICES = [
        ("active", "Actif"),
        ("inactive", "Inactif"),
        ("pending", "En attente"),
    ]

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="The phone number must be formatted: '+999999999'",
    )

    # Informations personnelles
    first_name = models.CharField(max_length=100, verbose_name="First name")
    last_name = models.CharField(max_length=100, verbose_name="Last name")
    birth_date = models.DateField(
        verbose_name="Date de naissance", null=True, blank=True
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name="Phone number",
    )

    # Adresse
    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Adresse"
    )
    city = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Ville"
    )
    postal_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Code postal"
    )

    # Relations et catégorisation
    roles = models.ManyToManyField(
        Role, related_name="members", default="Membres"
    )
    tags = models.ManyToManyField(
        Tag, related_name="members", blank=True, default="Escrimeur"
    )
    sports_category = models.ForeignKey(
        SportsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sports category",
    )

    # Statut et dates
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Statut",
    )
    date_joined = models.DateField(
        auto_now_add=True, verbose_name="Date of registration"
    )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name="Last update"
    )

    # Média
    photo = models.ImageField(
        upload_to="member_photos/", blank=True, null=True, verbose_name="Photo"
    )

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Membre"
        verbose_name_plural = "Membres"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_photo_url(self):
        return self.photo.url if self.photo else None

    def determine_sports_category(self):
        """Détermine la catégorie sportive en fonction de l'année de naissance."""
        for category in SportsCategory.objects.all():
            if category.is_applicable(self.birth_year):
                self.sports_category = category
                self.save()
                return category
        return None
