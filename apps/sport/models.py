from django.db import models
from django.utils.timezone import now
from django.db.models import UniqueConstraint


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


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    date = models.DateTimeField(
        verbose_name="Date de l'évènement", default=now
    )
    location = models.TextField(verbose_name="Lieu")
    participants = models.ManyToManyField(
        "members.Member", related_name="events", verbose_name="Participants"
    )

    class Meta:
        ordering = ["date"]

    def has_results(self):
        return self.results.exists()

    def is_upcoming(self):
        return self.date >= now()

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%d/%m/%Y %H:%M')}"


class Result(models.Model):
    event = models.ForeignKey(
        "Event",
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name="Évènement",
    )
    member = models.ForeignKey(
        "members.Member",
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name="Membre",
    )
    rank = models.PositiveIntegerField(
        verbose_name="Classement", null=True, blank=True
    )
    information = models.CharField(
        max_length=50, verbose_name="Information", null=True, blank=True
    )
    details = models.TextField(verbose_name="Détails du résultat", blank=True)

    class Meta:
        ordering = ["rank"]
        constraints = [
            UniqueConstraint(
                fields=["event", "member"], name="unique_event_member"
            )
        ]

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name} - {self.event.title} ({self.rank})"
