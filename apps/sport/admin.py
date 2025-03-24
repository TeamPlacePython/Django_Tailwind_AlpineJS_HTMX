from django.contrib import admin
from .models import SportsCategory

# Register your models here.


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
    ordering = ("-start_year",)
