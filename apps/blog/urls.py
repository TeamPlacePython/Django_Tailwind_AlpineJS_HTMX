from django.urls import path

from .views import BlogIndexView

app_name = "blog"

urlpatterns = [
    path("", BlogIndexView.as_view(), name="blog_index"),
]
