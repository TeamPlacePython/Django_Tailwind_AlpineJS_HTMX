from django.urls import path
from .views import TrainingHoursView, SportsCategoryListView

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
]
