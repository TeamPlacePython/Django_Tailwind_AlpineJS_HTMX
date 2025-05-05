from django.contrib import admin
from .models import MapsLocation


@admin.register(MapsLocation)
class MapsLocationAdmin(admin.ModelAdmin):
    list_display = (
        "station_name",
        "latitude",
        "longitude",
        "address",
    )
