from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Post,
    LikedPost,
    Tag,
    Comment,
    LikedComment,
    Reply,
    LikedReply,
)


# 📌 Personnalisation du modèle Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created")
    list_filter = ("created", "author", "tags")
    search_fields = ("title", "author__username")
    ordering = ("-created",)
    filter_horizontal = ("tags",)


# 📌 Personnalisation des Tags
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "image_tag")
    ordering = ("order",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def image_tag(self, obj):
        """Affiche l'image sous forme de vignette dans l'admin."""
        if obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 5px;" />',
                obj.image.url,
            )
        return "Aucune image"

    image_tag.short_description = "Aperçu"


# 📌 Personnalisation des Commentaires
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "parent_post", "created")
    list_filter = ("created", "author")
    search_fields = ("body", "author__username")


# 📌 Personnalisation des Réponses
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("author", "parent_comment", "created")
    list_filter = ("created", "author")
    search_fields = ("body", "author__username")


# 📌 Gestion des Likes (Lecture seule, car c'est juste un enregistrement)
@admin.register(LikedPost)
class LikedPostAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created")
    list_filter = ("created", "user")
    readonly_fields = ("user", "post", "created")


@admin.register(LikedComment)
class LikedCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "created")
    list_filter = ("created", "user")
    readonly_fields = ("user", "comment", "created")


@admin.register(LikedReply)
class LikedReplyAdmin(admin.ModelAdmin):
    list_display = ("user", "reply", "created")
    list_filter = ("created", "user")
    readonly_fields = ("user", "reply", "created")
