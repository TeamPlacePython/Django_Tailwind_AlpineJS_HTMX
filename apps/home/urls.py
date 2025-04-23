from django.urls import path

from .views import HomeIndexView, CarouselFragmentView, StationsMapFragmentView

app_name = "home"

urlpatterns = [
    path("", HomeIndexView.as_view(), name="home_index"),
    path(
        "carousel/",
        CarouselFragmentView.as_view(),
        name="carousel_fragment",
    ),
    path("map/", StationsMapFragmentView.as_view(), name="map_fragment"),
]
