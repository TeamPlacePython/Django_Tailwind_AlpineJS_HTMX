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
    path("@<username>/", ProfileView.as_view(), name="user_profile"),
    path("edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("onboarding/", ProfileEditView.as_view(), name="profile_onboarding"),
    path("settings/", ProfileSettingsView.as_view(), name="profile_settings"),
    path("delete/", ProfileDeleteView.as_view(), name="profile_delete"),
    path(
        "emailchange/",
        ProfileEmailChangeView.as_view(),
        name="profile_emailchange",
    ),
    path(
        "emailverify/",
        ProfileEmailVerifyView.as_view(),
        name="profile_emailverify",
    ),
    path(
        "usernamechange/",
        ProfileUsernameChangeView.as_view(),
        name="profile_username_change",
    ),
]
