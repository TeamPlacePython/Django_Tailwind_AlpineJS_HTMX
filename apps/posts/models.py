from django.db import models
from django.contrib.auth.models import User
import uuid

from apps.images.mixins import ImageResizeMixin


class Post(ImageResizeMixin, models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="post_images/")
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    body = models.TextField()
    likes = models.ManyToManyField(
        User, related_name="liked_posts", through="LikedPost"
    )
    tags = models.ManyToManyField("Tag", related_name="posts")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/post/{self.id}/"

    def save(self, *args, **kwargs):
        if self.image:
            self.resize_image_field(self.image)
        super().save(*args, **kwargs)


class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.post.title}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.FileField(upload_to="icons/", null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/category/{self.slug}/"


class Comment(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="comments"
    )
    parent_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.CharField(max_length=255)
    likes = models.ManyToManyField(
        User, related_name="liked_comments", through="LikedComment"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.author.username if self.author else 'Anonymous'} : {self.body[:30]}"


class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.comment.body[:30]}"


class Reply(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="replies"
    )
    parent_comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies"
    )
    body = models.CharField(max_length=255)
    likes = models.ManyToManyField(
        User, related_name="liked_replies", through="LikedReply"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.author.username if self.author else 'Anonymous'} : {self.body[:30]}"


class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.reply.body[:30]}"
