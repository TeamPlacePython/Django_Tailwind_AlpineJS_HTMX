from django.urls import path
from .views import (
    MemberListView,
    MemberTableView,
    MemberDetailView,
    MemberCreateView,
    MemberUpdateView,
    MemberDeleteView,
    UpdatePhotoView,
)

app_name = "members"

urlpatterns = [
    path("", MemberListView.as_view(), name="member_list"),
    path("table/", MemberTableView.as_view(), name="member_table"),
    path("member/<int:pk>/", MemberDetailView.as_view(), name="member_detail"),
    path("member/add/", MemberCreateView.as_view(), name="member_create"),
    path(
        "member/<int:pk>/edit/",
        MemberUpdateView.as_view(),
        name="member_update",
    ),
    path(
        "member/<int:pk>/delete/",
        MemberDeleteView.as_view(),
        name="member_delete",
    ),
    path(
        "member/<int:pk>/photo/update/",
        UpdatePhotoView.as_view(),
        name="update_photo",
    ),
]
