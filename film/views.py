from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Film, Like, Score
from .serializers import FilmSerializer
from .utils import FilmPagination
from accounts.authentication import AccessTokenAuthentication


# Create your views here.


class FilmList(ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    pagination_class = FilmPagination


class LikeFilm(APIView):
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        film_id = request.data.get("film_id")
        try:
            film = Film.objects.get(id=film_id)
        except Exception:
            return Response({"message": "film not found"}, status=status.HTTP_404_NOT_FOUND)

        like_obj, created = Like.objects.get_or_create(user=request.user, film=film)
        if not created:
            like_obj.delete()

        count = film.number_of_likes

        return Response({'like_count': count}, status=status.HTTP_200_OK)


class ScoreFilm(APIView):
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        film_id = request.data.get("film_id")
        score = request.data.get("score")
        try:
            film = Film.objects.get(id=film_id)
        except Exception:
            return Response({"message": "film not found"}, status=status.HTTP_404_NOT_FOUND)

        Score_obj, _ = Score.objects.get_or_create(user=request.user, film=film)

        Score_obj.score = score
        Score_obj.save()

        film_score = film.score_amounts

        return Response({'film_score': film_score}, status=status.HTTP_200_OK)
