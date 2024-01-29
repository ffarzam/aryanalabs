from rest_framework.pagination import PageNumberPagination


class FilmPagination(PageNumberPagination):
    page_size = 10