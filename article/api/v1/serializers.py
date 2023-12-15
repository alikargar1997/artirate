from rest_framework import serializers
from article.models import Article, Rating
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class ArticleSerializer(serializers.ModelSerializer):
    users_rates_count = serializers.IntegerField(source="total_user_rates_count")
    rates_average = serializers.FloatField(source="total_user_rates_avg")
    user_rate = serializers.IntegerField(source="user_max_rate")

    class Meta:
        model = Article
        fields = ("title", "text", "users_rates_count", "rates_average", "user_rate")


class RateArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("rate",)

    def save(self, **kwargs):
        user = self.context.get("user")
        article = self.context.get("article")
        rating = (
            Rating.custom_objects.filter(
                user=user,
                article=article,
            )
            .select_for_update()
            .first()
        )
        if not rating:
            rating = Rating(
                user=user,
                article=article,
            )
        rating.rate = self.validated_data.get("rate", 0)
        rating.save()
        return rating
