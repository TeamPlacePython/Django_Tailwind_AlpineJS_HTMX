from django.contrib import admin
from .models import MessageBoard, Message


@admin.register(MessageBoard)
class MessageBoardAdmin(admin.ModelAdmin):
    list_display = ("id",)
    filter_horizontal = ("subscribers",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("author", "body", "created", "messageboard")
    list_filter = ("created", "author")
    search_fields = ("body", "author__username")
