from django.urls import path

from core.views import (
    CreateAvowalView,
    ListAvowalView,
    DetailAvowalView,
    TopicFilterListView,
    PrivacyView,
)

app_name = "core"
urlpatterns = [
    path(
        "t/new/",
        CreateAvowalView.as_view(),
        name="create",
    ),
    path(
        "",
        ListAvowalView.as_view(),
        name="home",
    ),
    path(
        "<str:code>/",
        DetailAvowalView.as_view(),
        name="detail",
    ),
    path(
        "topic/<str:tag>/",
        TopicFilterListView.as_view(),
        name="topic-filter",
    ),
    path(
        "t/privacy/",
        PrivacyView.as_view(),
        name="privacy",
    ),
]
