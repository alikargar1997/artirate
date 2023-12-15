from django.db import models
from django.db.models.query import QuerySet
from django.db.models import FilteredRelation, Count, Avg, Q, Max


class ArticleCustomQuerySet(models.QuerySet):
    def with_rating_details(self, user_id: int):
        return self.annotate(
            total_user_rates_count=Count("users_rates__user_id"),
            total_user_rates_avg=Avg("users_rates__rate"),
            article_user_rates=FilteredRelation(
                "users_rates", condition=Q(users_rates__user_id=user_id)
            ),
            user_max_rate=Max("article_user_rates__rate"),
        )


class ArticleCustomManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return ArticleCustomQuerySet(self.model, using=self._db)

    def get_articles_with_rating_details(self, user_id: int):
        return self.get_queryset().with_rating_details(user_id)


class Article(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    objects = models.Manager()
    custom_objects = ArticleCustomManager()

    def __str__(self) -> str:
        return self.title
