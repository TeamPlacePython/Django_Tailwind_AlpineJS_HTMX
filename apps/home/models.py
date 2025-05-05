from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class MapsLocation(models.Model):
    station_name = models.CharField(max_length=250)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        help_text="Valeur entre -90 et 90.",
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        help_text="Valeur entre -180 et 180.",
    )
    address = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        unique_together = (
            "latitude",
            "longitude",
        )  # Évite les doublons de position

    def __str__(self):
        return self.station_name
