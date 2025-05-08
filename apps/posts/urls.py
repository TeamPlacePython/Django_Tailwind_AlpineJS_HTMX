from django.urls import path
from .views import (
    PostHomeView,
    PostDetailView,
    AddPostView,
    LikePostView,
    PostEditView,
    PostDeleteView,
    CommentCreateView,
    ReplyCreateView,
    CommentDeleteView,
    ReplyDeleteView,
    LastPostFragmentView,
)

app_name = "posts"

urlpatterns = [
    path("", PostHomeView.as_view(), name="post_home"),
    path("category/<tag>/", PostHomeView.as_view(), name="category"),
    path("create/", AddPostView.as_view(), name="add_post"),
    path("delete/<uuid:pk>/", PostDeleteView.as_view(), name="post_delete"),
    path("post/<uuid:pk>/edit/", PostEditView.as_view(), name="post_edit"),
    path("post/<uuid:pk>/", PostDetailView.as_view(), name="post_page"),
    path("post/like/<int:pk>/", LikePostView.as_view(), name="like_post"),
    path(
        "last_post_fragment/",
        LastPostFragmentView.as_view(),
        name="last_post_fragment",
    ),
]
