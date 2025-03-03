from django.urls import path

from . import views

app_name = "messageboard"

urlpatterns = [
    path("", views.MessageBoardView.as_view(), name="messageboard"),
    path("subscribe/", views.SubscribeView.as_view(), name="subscribe"),
    path("newsletter/", views.NewsletterView.as_view(), name="newsletter"),
]
