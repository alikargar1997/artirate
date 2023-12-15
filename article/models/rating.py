from django.db import models
from django.db.models.query import QuerySet
from django.core.validators import MinValueValidator, MaxValueValidator

class RatingCustomQuerySet(models.QuerySet):
    ...


class RatingCustomManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return RatingCustomQuerySet(self.model, using=self._db)


class Rating(models.Model):
    user = models.ForeignKey(
        "auth.User", on_delete=models.PROTECT, related_name="articles_rates"
    )
    article = models.ForeignKey(
        "article.Article", on_delete=models.PROTECT, related_name="users_rates"
    )
    rate = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    objects = models.Manager()
    custom_objects = RatingCustomManager()

    class Meta:
        unique_together = ("article", "user")

    def __str__(self) -> str:
        return f"{self.user.username}-{self.article.title}"
