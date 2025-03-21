from django.urls import path

from .views import MessageBoardView, SubscribeView, NewsletterView

app_name = "messageboard"

urlpatterns = [
    path("", MessageBoardView.as_view(), name="messageboard"),
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("newsletter/", NewsletterView.as_view(), name="newsletter"),
]
