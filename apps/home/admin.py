from django.contrib import admin
from .models import MapsLocation, CarouselImage, Event, Result


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


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("event", "member", "rank", "information", "details")
