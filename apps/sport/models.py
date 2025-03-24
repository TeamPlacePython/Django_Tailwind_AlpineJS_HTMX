from django.db import models


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
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

    def is_applicable(self, birth_year):
        """Checks if this category applies based on the member's birth year."""
        if self.start_year and self.end_year:
            return self.start_year <= birth_year <= self.end_year
        return False
