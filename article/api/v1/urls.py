from django.urls import path
from article.api.v1.views import ArticleListApiView,RateArticleApiView

urlpatterns = [
    path("articles/", ArticleListApiView.as_view(), name="list-articles-v1"),
    path("articles/<pk>/", RateArticleApiView.as_view(), name="rate-article-v1"),
]
