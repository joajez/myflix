from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


from .models import Movie, Genre
from .serializers import MovieSerializer, GenreSerializer


# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # permission_classes = [IsAuthenticated]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = [IsAuthenticated]
