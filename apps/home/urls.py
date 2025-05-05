from django.urls import path
from .views import HomeIndexView, StationsMapFragmentView

app_name = "home"

urlpatterns = [
    path("", HomeIndexView.as_view(), name="home_index"),
    path("map/", StationsMapFragmentView.as_view(), name="map_fragment"),
]
