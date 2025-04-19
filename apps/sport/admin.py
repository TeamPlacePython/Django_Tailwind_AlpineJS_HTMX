from django.contrib import admin
from .models import SportsCategory, Event, Result


@admin.register(SportsCategory)
class SportsCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_year",
        "end_year",
        "fee_amount",
        "created_at",
    )
    list_filter = ("start_year", "end_year")
    search_fields = ("name",)
    readonly_fields = ("created_at",)
    fieldsets = (
        (
            "Informations générales",
            {
                "fields": (
                    "name",
                    "description",
                    "start_year",
                    "end_year",
                    "fee_amount",
                )
            },
        ),
        (
            "Horaires",
            {
                "fields": (
                    "monday_hours",
                    "tuesday_hours",
                    "wednesday_hours",
                    "thursday_hours",
                    "friday_hours",
                ),
            },
        ),
        (
            "Autres",
            {
                "fields": ("created_at",),
            },
        ),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location", "is_upcoming", "has_results")
    list_filter = ("date",)
    search_fields = ("title", "location")
    autocomplete_fields = ("participants",)
    filter_horizontal = ("participants",)
    readonly_fields = ("is_upcoming", "has_results")

    def is_upcoming(self, obj):
        return obj.is_upcoming()

    is_upcoming.boolean = True  # Affiche un check ✔️ dans l'admin

    def has_results(self, obj):
        return obj.has_results()

    has_results.boolean = True


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("event", "member", "rank", "information")
    list_filter = ("event", "rank")
    search_fields = ("member__first_name", "member__last_name", "event__title")
    autocomplete_fields = ("member",)
    ordering = ("rank",)
