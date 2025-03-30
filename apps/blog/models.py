from django.db import models
from django.contrib.auth.models import User
import uuid


class Blog(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="blogs"
    )
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images/")
    tags = models.ManyToManyField("Tag", blank=True)
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
