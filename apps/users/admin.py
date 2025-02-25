from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "displayname",
        "created_at",
        "updated_at",
        "is_staff",
    )
    list_filter = ("created_at", "updated_at", "is_staff")
    search_fields = ("user__username", "displayname")
    readonly_fields = ("created_at", "updated_at")

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_staff:
            return (
                (
                    _("Informations utilisateur"),
                    {"fields": ("user", "displayname")},
                ),
                (_("Informations supplémentaires"), {"fields": ("info",)}),
                (
                    _("Métadonnées"),
                    {
                        "fields": ("created_at", "updated_at"),
                        "classes": ("collapse",),
                    },
                ),
            )
        return (
            (
                _("Informations utilisateur"),
                {"fields": ("user", "displayname")},
            ),
            (_("Médias"), {"fields": ("image",)}),
            (_("Informations supplémentaires"), {"fields": ("info",)}),
            (
                _("Métadonnées"),
                {
                    "fields": ("created_at", "updated_at"),
                    "classes": ("collapse",),
                },
            ),
            (_("Permissions"), {"fields": ("is_staff",)}),
        )
