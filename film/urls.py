from django.urls import path
from . import views


urlpatterns = [
    path('film_list/', views.FilmList.as_view(), name='film_list'),
    path('like_film/', views.LikeFilm.as_view(), name='like_film'),
    path('score_film/', views.ScoreFilm.as_view(), name='score_film'),

]
