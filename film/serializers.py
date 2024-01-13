from rest_framework import serializers

from .models import Film


class FilmSerializer(serializers.ModelSerializer):
    liked_count = serializers.SerializerMethodField()
    score_amount = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = ["id", "name", "year", "genre", "liked_count", "score_amount"]

    def get_liked_count(self, obj):
        return obj.number_of_likes

    def get_score_amount(self, obj):
        return obj.score_amounts
