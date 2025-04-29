from django.urls import path
from .views import (
    MemberListView,
    MemberTableView,
    MemberEditView,
    MemberCreateView,
    MemberUpdateView,
    MemberDeleteView,
    MemberPhotoUpdateView,
    ResetMemberStatusView,
    MemberHomeView,
)

app_name = "members"

urlpatterns = [
    path("", MemberListView.as_view(), name="member_list"),
    path("table/", MemberTableView.as_view(), name="member_table"),
    path("member/<int:pk>/", MemberEditView.as_view(), name="member_edit"),
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
        MemberPhotoUpdateView.as_view(),
        name="update_photo",
    ),
    path(
        "reset-status/",
        ResetMemberStatusView.as_view(),
        name="reset_member_status",
    ),
    path(
        "random-members/",
        MemberHomeView.as_view(),
        name="random_members",
    ),
]
