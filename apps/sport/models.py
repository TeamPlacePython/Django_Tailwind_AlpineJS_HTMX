from django.db import models
from django.apps import apps


class SportsCategory(models.Model):
    """Age category for fencing practice."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    fee_amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Membership Fee (€)",
        help_text="Montant de la cotisation pour cette catégorie",
    )
    monday_hours = models.CharField(max_length=50, blank=True, null=True)
    tuesday_hours = models.CharField(max_length=50, blank=True, null=True)
    wednesday_hours = models.CharField(max_length=50, blank=True, null=True)
    thursday_hours = models.CharField(max_length=50, blank=True, null=True)
    friday_hours = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Sports categories"
        ordering = ["-start_year"]

    def __str__(self):
        return f"{self.name}"

    def is_applicable(self, birth_year):
        """Checks if this category applies based on the member's birth year."""
        if self.start_year and self.end_year:
            return self.start_year <= birth_year <= self.end_year
        return False


class Performance(models.Model):
    member = models.ForeignKey(
        "members.Member", on_delete=models.CASCADE, related_name="performances"
    )
    title = models.CharField(
        max_length=200, verbose_name="Titre de la performance"
    )
    description = models.TextField(verbose_name="Détails de la performance")
    creation_date = models.DateField(verbose_name="Date de réalisation")

    class Meta:
        verbose_name = "Performance"
        verbose_name_plural = "Performances"
        ordering = ["-creation_date"]

    def __str__(self):
        return f"{self.title} - {self.member}"

    @staticmethod
    def check_member_model_exists():
        try:
            # Checks if the "Member" template exists in the "members" application
            model = apps.get_model("members", "Member")
            return True
        except LookupError:
            # The template was not found
            return False


class Results(models.Model):
    member = models.ForeignKey(
        "members.Member", on_delete=models.CASCADE, related_name="resultats"
    )
    event = models.CharField(max_length=200, verbose_name="Événement")
    position = models.PositiveIntegerField(verbose_name="Position obtenue")
    date_event = models.DateField(verbose_name="Date de l'événement")
    comment = models.TextField(blank=True, verbose_name="Commentaire")

    class Meta:
        verbose_name = "Résultat"
        verbose_name_plural = "Résultats"
        ordering = ["-date_event"]

    def __str__(self):
        return f"{self.event} - {self.member} : {self.position}ᵉ place"
