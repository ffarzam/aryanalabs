from datetime import datetime

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.views import APIView

from .models import Film, Like, Score
from .serializers import FilmSerializer,FilmWithCritiquesSerializer
from .utils import FilmPagination
from accounts.authentication import AccessTokenAuthentication
from imdb.elastic import ES_CONNECTION
from .documents import FILMS_SEARCH_FIELDS,CRITIQUE_SEARCH_FIELDS

# Create your views here.

index_name = "task"


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



class SearchFilmView(APIView):
    def get(self, request, *args, **kwargs):
        print(request.GET)

        query_dict = {}
        for query_api_name,query_db_name in FILMS_SEARCH_FIELDS.items():
            if value:=request.GET.get(query_api_name):
                print(f"{query_db_name}: {value}")
                query_dict[query_db_name] = value

        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match":
                            {
                                query_db_name: value
                            }
                        } for query_db_name,value in query_dict.items()
                    ]
                }
            }
        }

        try:
            result = ES_CONNECTION.search(index=index_name, body=query)
            print(result)
            hits = result['hits']['hits']
            response_data = [{'id': hit['_id'], 'source': hit['_source']} for hit in hits]
            return JsonResponse({'data': response_data})

        except Exception as e:
            raise e
            return JsonResponse({'error': str(e)}, status=500)

