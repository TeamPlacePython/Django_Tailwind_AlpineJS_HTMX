from django.urls import path
from .views import (
    SportsCategoryListView,
    TrainingHoursView,
    ResultsListView,
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
]
