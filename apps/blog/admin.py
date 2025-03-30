from django.contrib import admin
from .models import (
    Blog,
    LikedBlog,
    Comment,
    LikedComment,
    Reply,
    LikedReply,
    Tag,
)


class LikedBlogInline(admin.TabularInline):
    model = LikedBlog
    extra = 1
    readonly_fields = ["user", "created"]
    can_delete = False
    show_change_link = True


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created", "updated", "get_tags")
    list_filter = ("created", "author", "tags")
    search_fields = ("title", "content", "tags__name")
    inlines = [LikedBlogInline]
    readonly_fields = ("created", "updated")

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    get_tags.short_description = "Tags"


class LikedCommentInline(admin.TabularInline):
    model = LikedComment
    extra = 1
    readonly_fields = ["user", "created"]
    can_delete = False
    show_change_link = True


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "parent_blog", "body", "created")
    list_filter = ("created", "author", "parent_blog")
    search_fields = ("body", "author__username", "parent_blog__title")
    inlines = [LikedCommentInline]
    readonly_fields = ("created",)


class LikedReplyInline(admin.TabularInline):
    model = LikedReply
    extra = 1
    readonly_fields = ["user", "created"]
    can_delete = False
    show_change_link = True


class ReplyAdmin(admin.ModelAdmin):
    list_display = ("author", "parent_comment", "body", "created")
    list_filter = ("created", "author", "parent_comment")
    search_fields = ("body", "author__username", "parent_comment__body")
    inlines = [LikedReplyInline]
    readonly_fields = ("created",)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "get_image_preview")
    search_fields = ("name", "slug")
    prepopulated_fields = {
        "slug": ("name",)
    }  # Automatically generate slug from name

    def get_image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-width: 50px; height: auto;" />'
        return "No Image"

    get_image_preview.allow_tags = True
    get_image_preview.short_description = "Image Preview"


class LikedBlogAdmin(admin.ModelAdmin):
    list_display = ("user", "blog", "created")
    list_filter = ("created", "user", "blog")
    search_fields = ("user__username", "blog__title")


class LikedCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "created")
    list_filter = ("created", "user", "comment")
    search_fields = ("user__username", "comment__body")


class LikedReplyAdmin(admin.ModelAdmin):
    list_display = ("user", "reply", "created")
    list_filter = ("created", "user", "reply")
    search_fields = ("user__username", "reply__body")


# Register the models with their corresponding admin configurations
admin.site.register(Blog, BlogAdmin)
admin.site.register(LikedBlog, LikedBlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LikedComment, LikedCommentAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(LikedReply, LikedReplyAdmin)
admin.site.register(Tag, TagAdmin)
