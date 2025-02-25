from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("", views.ProfileView.as_view(), name="profile"),
    path("@<username>/", views.ProfileView.as_view(), name="profile"),
    path("edit/", views.ProfileEditView.as_view(), name="profile-edit"),
    path(
        "onboarding/",
        views.ProfileEditView.as_view(),
        name="profile-onboarding",
    ),
    path(
        "settings/",
        views.ProfileSettingsView.as_view(),
        name="profile-settings",
    ),
    path(
        "emailchange/",
        views.ProfileEmailChangeView.as_view(),
        name="profile-emailchange",
    ),
    path(
        "emailverify/",
        views.ProfileEmailVerifyView.as_view(),
        name="profile-emailverify",
    ),
    path("delete/", views.ProfileDeleteView.as_view(), name="profile-delete"),
    path(
        "usernamechange/",
        views.ProfileUsernameChangeView.as_view(),
        name="profile-username-change",
    ),
]
