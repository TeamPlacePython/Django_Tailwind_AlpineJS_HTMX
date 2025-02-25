from django.urls import path
from .views import (
    MemberListView,
    MemberDetailView,
    MemberCreateView,
    MemberUpdateView,
    MemberDeleteView,
    update_member_photo,
)

app_name = "members"

urlpatterns = [
    path("", MemberListView.as_view(), name="member-list"),
    path("member/<int:pk>/", MemberDetailView.as_view(), name="member-detail"),
    path("member/add/", MemberCreateView.as_view(), name="member-create"),
    path(
        "member/<int:pk>/edit/",
        MemberUpdateView.as_view(),
        name="member-update",
    ),
    path(
        "member/<int:pk>/delete/",
        MemberDeleteView.as_view(),
        name="member-delete",
    ),
    path(
        "member/<int:pk>/update-photo/",
        update_member_photo,
        name="update-photo",
    ),
]
