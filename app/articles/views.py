from typing import Any

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from app.articles.models import Article
from app.articles.permissions import AuthorOrReadOnly
from app.articles.serializers import ArticlesSerializers


class ArticleListCreateView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticated,
        AuthorOrReadOnly,
    ]
    serializer_class = ArticlesSerializers
    lookup_field = "user"
    queryset = Article.objects.all()
    renderer_classes = [
        JSONRenderer,
    ]


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticated,
        AuthorOrReadOnly,
    ]
    serializer_class = ArticlesSerializers
    lookup_field = "slug"
    queryset = Article.objects.all()
    renderer_classes = [
        JSONRenderer,
    ]

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Returns message on deletion of articles
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Article deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )