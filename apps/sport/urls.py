from django.urls import path
from .views import (
    SportsCategoryListView,
    TrainingHoursView,
    ResultsListView,
    ResultEventHomeView,
    UpcomingEventHomeView,
)

app_name = "sport"

urlpatterns = [
    path(
        "cotisations/",
        SportsCategoryListView.as_view(),
        name="sport_category_cotisations",
    ),
    path(
        "training-hours/",
        TrainingHoursView.as_view(),
        name="sport_training_hours",
    ),
    path("results/", ResultsListView.as_view(), name="results_list"),
    path(
        "home_results_events/",
        ResultEventHomeView.as_view(),
        name="home_results_events",
    ),
    path(
        "home_upcoming_events/",
        UpcomingEventHomeView.as_view(),
        name="home_upcoming_events",
    ),
]
