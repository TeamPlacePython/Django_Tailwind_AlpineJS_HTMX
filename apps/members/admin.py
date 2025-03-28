from django.contrib import admin
from django.utils.html import format_html
from .models import Member, Tag, MembershipFee


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Admin panel configuration for Members."""

    list_display = (
        "first_name",
        "last_name",
        "birth_date",
        "email",
        "phone_number",
        "roles",
        "status",
        "sports_category",
        "date_joined",
        "display_photo",
    )
    list_filter = ("status", "sports_category", "roles", "tags")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("last_name", "first_name")

    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "gender",
                    "first_name",
                    "last_name",
                    "birth_date",
                    "email",
                    "phone_number",
                    "photo",
                )
            },
        ),
        (
            "Address",
            {
                "fields": (
                    "address",
                    "address_complement",
                    "postal_code",
                    "city",
                )
            },
        ),
        (
            "Categorization",
            {
                "fields": (
                    "roles",
                    "handeness",
                    "tags",
                    "weapon",
                    "sports_category",
                )
            },
        ),
        ("Status", {"fields": ("status",)}),
    )

    def display_photo(self, obj):
        """
        Displays a small preview of the member's photo in the admin panel.
        """
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:5px;" />',
                obj.photo.url,
            )
        return "No Photo"

    display_photo.short_description = "Photo"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin panel for managing tags."""

    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(MembershipFee)
class MembershipFeeAdmin(admin.ModelAdmin):
    """Admin panel for tracking membership fees and payments."""

    list_display = ("member", "is_valid")
    list_filter = ("is_valid",)
    search_fields = ("member__first_name", "member__last_name")
    ordering = ("member",)
