from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image
from io import BytesIO


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


def validate_image_format(image):
    """Vérifie que l'image est bien un format JPEG ou PNG valide."""
    try:
        img = Image.open(image)
        img.verify()  # Vérification de base
        img = Image.open(
            image
        )  # Recharge pour s'assurer qu'elle peut être manipulée
        if img.format not in ("JPEG", "PNG"):
            raise ValidationError(
                "Seuls les formats JPEG et PNG sont autorisés."
            )
    except Exception as e:
        raise ValidationError(
            "Téléversez une image valide (JPEG ou PNG)."
        ) from e


class CarouselImage(models.Model):
    image = models.ImageField(
        upload_to="carousel_images/",
        validators=[
            validate_image_format
        ],  # Ajout de la validation dès l’upload
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Image {self.id} - {self.image.name}"

    def clean(self):
        """Valide que l'image est au format paysage avant l'enregistrement."""
        if not self.image:
            return

        img = Image.open(self.image)
        width, height = img.size
        if width <= height:
            raise ValidationError(
                "L'image doit être au format paysage (largeur > hauteur)."
            )

    def save(self, *args, **kwargs):
        """Redimensionne et reformate l'image avant de l'enregistrer."""
        if not self.image:
            return  # Empêche une erreur si aucune image n'est fournie

        # Ouvre l'image
        img = Image.open(self.image)

        # Vérifie si l'image est déjà en JPEG, sinon la convertit
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Redimensionnement
        target_size = (1920, 1080)
        img = img.resize(target_size, Image.LANCZOS)

        # Sauvegarde dans un buffer en mémoire
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=90)

        # Génère un nom d'image unique pour éviter l'écrasement des fichiers
        image_name = f"carousel_{self.image.name or 'new'}"

        # Réécriture de l'image dans l'instance
        self.image.save(image_name, ContentFile(buffer.getvalue()), save=False)

        # Sauvegarde finale en base de données
        super().save(*args, **kwargs)
