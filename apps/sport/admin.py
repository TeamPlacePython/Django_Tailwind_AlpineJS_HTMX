from django.contrib import admin
from .models import SportsCategory, Performance, Results


@admin.register(SportsCategory)
class SportsCategoryAdmin(admin.ModelAdmin):
    """Admin panel for managing sports categories."""

    list_display = (
        "name",
        "description",
        "start_year",
        "end_year",
        "fee_amount",
        "created_at",
        "monday_hours",
        "tuesday_hours",
        "wednesday_hours",
        "thursday_hours",
        "friday_hours",
    )
    search_fields = ("name",)


@admin.register(Performance)
class Performance(admin.ModelAdmin):
    list_display = (
        "member",
        "title",
        "description",
        "creation_date",
    )
    search_fields = ("member",)
    ordering = ["-creation_date"]


@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "event",
        "position",
        "date_event",
        "comment",
    )
    search_fields = ("name",)
    ordering = ["-date_event"]
