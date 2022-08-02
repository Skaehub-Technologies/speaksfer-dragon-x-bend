from django.urls import path

from app.articles.views import ArticleDetailView, ArticleListCreateView

urlpatterns = [
    path("articles/", ArticleListCreateView.as_view(), name="article-list"),
    path(
        "article/<slug:slug>/",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
]
