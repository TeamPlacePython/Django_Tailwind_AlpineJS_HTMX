from django.contrib import admin
from django.utils.html import format_html
from .models import Image, CarouselImage


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "uploaded_at")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "title",
        "uploaded_by",
        "uploaded_at",
    )
    list_filter = ("uploaded_by", "uploaded_at")
    search_fields = ("title", "description", "uploaded_by__username")
    readonly_fields = ("uploaded_at", "image_preview")
    fields = (
        "title",
        "image",
        "image_preview",
        "uploaded_by",
        "uploaded_at",
    )
    ordering = ("-uploaded_at",)

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: auto; border-radius: 4px;" />',
                obj.image.url,
            )
        return "-"

    thumbnail.short_description = "Preview"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px;" />',
                obj.image.url,
            )
        return "No image"

    image_preview.short_description = "Image Preview"
