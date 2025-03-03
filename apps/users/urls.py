from django.urls import path

from .views import (
    ProfileView,
    ProfileEditView,
    ProfileSettingsView,
    ProfileEmailChangeView,
    ProfileEmailVerifyView,
    ProfileDeleteView,
    ProfileUsernameChangeView,
)

app_name = "users"

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("@<username>/", ProfileView.as_view(), name="profile"),
    path("edit/", ProfileEditView.as_view(), name="profile-edit"),
    path("onboarding/", ProfileEditView.as_view(), name="profile-onboarding"),
    path("settings/", ProfileSettingsView.as_view(), name="profile-settings"),
    path("delete/", ProfileDeleteView.as_view(), name="profile-delete"),
    path(
        "emailchange/",
        ProfileEmailChangeView.as_view(),
        name="profile-emailchange",
    ),
    path(
        "emailverify/",
        ProfileEmailVerifyView.as_view(),
        name="profile-emailverify",
    ),
    path(
        "usernamechange/",
        ProfileUsernameChangeView.as_view(),
        name="profile-username-change",
    ),
]
