from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image as PilImage
from .mixins import ImageResizeMixin


def validate_image_format(image):
    valid_extensions = ["jpg", "jpeg", "png"]
    ext = image.name.split(".")[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            "Seuls les formats JPG, JPEG ou PNG sont autorisés."
        )


class CarouselImage(ImageResizeMixin, models.Model):
    image = models.ImageField(
        upload_to="carousel_images/",
        validators=[validate_image_format],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_images",
    )

    IMAGE_RESIZE_MODE = "resize"
    TARGET_SIZE = (1920, 1080)
    FORCE_LANDSCAPE = True

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Image {self.id} - {self.image.name}"

    def clean(self):
        if not self.image:
            return
        img = PilImage.open(self.image)
        width, height = img.size
        if width <= height:
            raise ValidationError(
                "L'image doit être au format paysage (largeur > hauteur)."
            )

    def save(self, *args, **kwargs):
        if self.image:
            self.resize_image_field(self.image)
        super().save(*args, **kwargs)


class Image(ImageResizeMixin, models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/")
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="post_uploaded_images",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image:
            self.resize_image_field(self.image)
        super().save(*args, **kwargs)
