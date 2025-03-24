from django.urls import path
from .views import (
    MemberListView,
    MemberTableView,
    MemberDetailView,
    MemberCreateView,
    MemberUpdateView,
    MemberDeleteView,
    UpdatePhotoView,
    # SportsCategoryListView,
    # TrainingHoursView,
)

app_name = "members"

urlpatterns = [
    path("", MemberListView.as_view(), name="member-list"),
    path("table/", MemberTableView.as_view(), name="member-table"),
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
        "member/<int:pk>/photo/update/",
        UpdatePhotoView.as_view(),
        name="update-photo",
    ),
]
