from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="articles/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="sections"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="sections/", blank=True, null=True)

    def __str__(self):
        return self.title


class Athlete(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="athletes/", blank=True, null=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="athletes"
    )

    def __str__(self):
        return self.name
