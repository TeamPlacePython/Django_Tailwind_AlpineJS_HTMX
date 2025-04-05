from django.urls import path
from .views import PostIndexView, PostDetailView, PostCreateView, LikePostView

app_name = "posts"

urlpatterns = [
    path("post/", PostIndexView.as_view(), name="post_index"),
    path("category/<tag>/", PostIndexView.as_view(), name="category"),
    path("create/", PostCreateView.as_view(), name="post_created"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_page"),
    path("post/like/<int:pk>/", LikePostView.as_view(), name="like_post"),
]
