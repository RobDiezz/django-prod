from django.urls import path, include

from .views import (
    ArticleListView,
    ArticleDetailView,
    LatestArticlesFeed,
)

app_name = "blogapp"

urlpatterns = [
    path("article/", ArticleListView.as_view(), name="article"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="article_details"),
    path("article/latest/feed/", LatestArticlesFeed(), name="articles-feed"),
]
