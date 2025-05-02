from django.urls import path
from .views import (
    SportsCategoryListView,
    TrainingHoursView,
    ResultsEventListView,
    ResultEventFragmentView,
    UpcomingEventFragmentView,
)

app_name = "sport"

urlpatterns = [
    path(
        "cotisations/",
        SportsCategoryListView.as_view(),
        name="sport_category_cotisations",
    ),
    path(
        "training_hours/",
        TrainingHoursView.as_view(),
        name="training_hours",
    ),
    path(
        "results/", ResultsEventListView.as_view(), name="results_event_list"
    ),
    path(
        "results_events_fragment/",
        ResultEventFragmentView.as_view(),
        name="results_events_fragment",
    ),
    path(
        "upcoming_events_fragment/",
        UpcomingEventFragmentView.as_view(),
        name="upcoming_events_fragment",
    ),
]
