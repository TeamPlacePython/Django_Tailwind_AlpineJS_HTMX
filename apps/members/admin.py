from django.contrib import admin
from .models import Member, Role, Tag, SportsCategory


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "birth_date",
        "email",
        "status",
        "sports_category",
        "date_joined",
    )
    list_filter = ("status", "sports_category", "roles", "tags")
    search_fields = ("first_name", "last_name", "email")
    filter_horizontal = ("roles", "tags")
    fieldsets = (
        (
            "Informations personnelles",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birth_date",
                    "email",
                    "phone_number",
                    "photo",
                )
            },
        ),
        ("Adresse", {"fields": ("address", "city", "postal_code")}),
        ("Catégorisation", {"fields": ("roles", "tags", "sports_category")}),
        ("Statut", {"fields": ("status",)}),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(SportsCategory)
class SportsCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "start_year",
        "end_year",
        "created_at",
    )
    search_fields = ("name",)
