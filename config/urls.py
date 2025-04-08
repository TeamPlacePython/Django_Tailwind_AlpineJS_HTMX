from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("apps.home.urls", namespace="home")),
    path("profile/", include("apps.users.urls", namespace="users")),
    path("members/", include("apps.members.urls", namespace="members")),
    path("sport/", include("apps.sport.urls", namespace="sport")),
    path("posts/", include("apps.posts.urls", namespace="posts")),
    path("history/", include("apps.history.urls", namespace="history")),
    path(
        "messageboard/",
        include("apps.messageboard.urls", namespace="messageboard"),
    ),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from debug_toolbar.toolbar import debug_toolbar_urls
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += debug_toolbar_urls()
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
