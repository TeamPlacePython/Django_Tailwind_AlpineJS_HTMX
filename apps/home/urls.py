from django.urls import path

from .views import HomeIndexView, ResultsListView

app_name = "home"

urlpatterns = [
    path("", HomeIndexView.as_view(), name="home-index"),
    path("results/", ResultsListView.as_view(), name="results_list"),
]
