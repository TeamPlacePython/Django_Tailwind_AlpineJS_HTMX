from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image as PilImage


def validate_image_format(image):
    valid_extensions = ["jpg", "jpeg", "png"]
    ext = image.name.split(".")[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            "Seuls les formats JPG, JPEG ou PNG sont autorisés."
        )


class CarouselImage(models.Model):
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
        if not self.image:
            return
        img = PilImage.open(self.image)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img = img.resize((1920, 1080), PilImage.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        image_name = f"carousel_{self.image.name or 'new'}"
        self.image.save(image_name, ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)


class Image(models.Model):
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
