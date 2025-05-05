from django.urls import path

from .views import (
    CarouselFragmentView,
    ImageWallView,
    ImageDownloadView,
    LastImageFragmentView,
)

app_name = "images"

urlpatterns = [
    path(
        "carousel/",
        CarouselFragmentView.as_view(),
        name="carousel_fragment",
    ),
    path("image_wall/", ImageWallView.as_view(), name="image_wall"),
    path(
        "download/<int:pk>/",
        ImageDownloadView.as_view(),
        name="image_download",
    ),
    path(
        "last_image_fragment",
        LastImageFragmentView.as_view(),
        name="last_image_fragment",
    ),
]
