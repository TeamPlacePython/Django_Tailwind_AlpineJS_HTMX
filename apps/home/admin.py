from django.contrib import admin
from .models import MapsLocation, CarouselImage


@admin.register(MapsLocation)
class MapsLocationAdmin(admin.ModelAdmin):
    list_display = (
        "station_name",
        "latitude",
        "longitude",
        "address",
    )


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "uploaded_at")
