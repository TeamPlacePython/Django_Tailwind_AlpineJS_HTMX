from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils.timezone import now
from PIL import Image
from io import BytesIO
import uuid


class Blog(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="blogs"
    )
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images/")
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)  # Coordonnées GPS
    longitude = models.FloatField(null=True, blank=True)
    tags = models.ManyToManyField("Tag", blank=True)  # Ajout des tags
    likes = models.ManyToManyField(
        User, related_name="liked_blogs", through="LikedBlog"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return f"/blog/{self.id}"


class LikedBlog(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} aime {self.blog.title}"


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="comments"
    )
    parent_blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(
        User, related_name="liked_comments", through="LikedComment"
    )
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return f"{self.author.username} : {self.body[:30]}"

    class Meta:
        ordering = ["-created"]


class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} aime "{self.comment.body[:30]}"'


class Reply(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="replies"
    )
    parent_comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies"
    )
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(
        User, related_name="liked_replies", through="LikedReply"
    )
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return f"{self.author.username} : {self.body[:30]}"

    class Meta:
        ordering = ["created"]


class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} aime "{self.reply.body[:30]}"'


class Tag(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to="icons/", null=True, blank=True)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]

    def get_absolute_url(self):
        return f"/category/{self.slug}/"


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
        img.verify()  # Vérifie si c'est une vraie image
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
            return  # Empêche une erreur si aucune image n'est fournie
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
        Event,
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
    score = models.CharField(
        max_length=50, verbose_name="Score", null=True, blank=True
    )
    details = models.TextField(verbose_name="Détails du résultat", blank=True)

    class Meta:
        unique_together = (
            "event",
            "member",
        )  # Chaque membre ne peut avoir qu'un seul résultat par événement

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name} - {self.event.title} ({self.rank})"
