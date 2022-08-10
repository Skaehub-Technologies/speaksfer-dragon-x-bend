from django.urls import path

from app.articles.views import (
    ArticleBookmarkView,
    ArticleCommentDetailView,
    ArticleCommentView,
    ArticleDetailView,
    ArticleFavouriteView,
    ArticleListCreateView,
    ArticleRatingsListCreateView,
    ArticleUnFavouriteView,
)

urlpatterns = [
    path("article/", ArticleListCreateView.as_view(), name="article-list"),
    path(
        "article/<slug:slug>/",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
    path("bookmarks/", ArticleBookmarkView.as_view(), name="bookmark"),
    path("comments/", ArticleCommentView.as_view(), name="comment"),
    path(
        "comments/<str:comment_id>/",
        ArticleCommentDetailView.as_view(),
        name="comment-delete",
    ),
    path("rate/", ArticleRatingsListCreateView.as_view(), name="rate"),
    path(
        "articles/<slug:slug>/favourite/",
        ArticleFavouriteView.as_view(),
        name="favourite",
    ),
    path(
        "articles/<slug:slug>/unfavourite/",
        ArticleUnFavouriteView.as_view(),
        name="unfavourite",
    ),
]
