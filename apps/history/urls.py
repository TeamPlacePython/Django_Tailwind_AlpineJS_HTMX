from django.urls import path
from .views import HistoryView

app_name = "history"

urlpatterns = [
    path("history/", HistoryView.as_view(), name="history"),
]
