from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO


class MapsLocation(models.Model):
    station_name = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.station_name


def validate_image_format(image):
    """Vérifie que le fichier uploadé est bien une image valide"""
    try:
        img = Image.open(image)
        img.verify()
    except Exception as e:
        raise ValidationError(
            "Téléversez une image valide (JPEG ou PNG)."
        ) from e


class CarouselImage(models.Model):
    image = models.ImageField(upload_to="carousel_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Image {self.id} - {self.image.name}"

    def clean(self):
        """Vérifie que l'image est au format paysage avant l'enregistrement"""
        if not self.image:
            return
        img = Image.open(self.image)
        width, height = img.size
        if width <= height:
            raise ValidationError(
                "L'image doit être au format paysage (largeur > hauteur)."
            )

    def save(self, *args, **kwargs):
        """Redimensionne et reformate l'image avant de l'enregistrer"""
        if not self.image:
            return  # Empêche une erreur si aucune image n'est fournie

        # Ouvre l'image avant la sauvegarde
        img = Image.open(self.image)

        # Vérification du format et redimensionnement
        target_size = (1920, 1080)
        img = img.convert("RGB")
        img = img.resize(target_size, Image.LANCZOS)

        # Sauvegarde dans un buffer en mémoire
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=90)

        # Réécriture de l'image dans l'instance
        self.image.save(
            self.image.name, ContentFile(buffer.getvalue()), save=False
        )

        # Sauvegarde finale en base de données
        super().save(*args, **kwargs)


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    date = models.DateTimeField(verbose_name="Date de l'évènement")
    location = models.TextField(verbose_name="Lieu")
    participants = models.ManyToManyField(
        "members.Member", related_name="events", verbose_name="Participants"
    )

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
        unique_together = (
            "event",
            "member",
        )  # Chaque membre ne peut avoir qu'un seul résultat par événement

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name} - {self.event.title} ({self.rank})"
