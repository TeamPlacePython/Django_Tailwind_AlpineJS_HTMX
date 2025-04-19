from django.urls import path
from .views import (
    PostIndexView,
    PostDetailView,
    PostCreateView,
    LikePostView,
    PostEditView,
)

app_name = "posts"

urlpatterns = [
    path("post/", PostIndexView.as_view(), name="post_index"),
    path("category/<tag>/", PostIndexView.as_view(), name="category"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("post/<uuid:pk>/", PostDetailView.as_view(), name="post_page"),
    path("post/like/<int:pk>/", LikePostView.as_view(), name="like_post"),
    path("post/<uuid:pk>/edit/", PostEditView.as_view(), name="post_edit"),
]
