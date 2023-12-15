from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    GenericAPIView,
)
from rest_framework import status
from rest_framework.views import APIView
from article.api.v1.serializers import ArticleSerializer, RateArticleSerializer
from article.models import Article
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ArticleListApiView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Article.custom_objects.get_articles_with_rating_details(
            user_id=self.request.user.id
        )


class RateArticleApiView(GenericAPIView):
    serializer_class = RateArticleSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Article.custom_objects

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"article": self.get_object(), "user": self.request.user})
        return context
