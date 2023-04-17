from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import CrewMember, Genre, Movie, CrewMember, CastMember
from .serializers import (
    CrewMemberSerializer,
    GenreSerializer,
    MovieSerializer,
    CastMemberSerializer,
)


# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["language", "genres"]
    search_fields = ["title"]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]


class CrewMemberViewSet(viewsets.ModelViewSet):
    queryset = CrewMember.objects.all()
    serializer_class = CrewMemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["movie", "department"]


class CastMemberViewSet(viewsets.ModelViewSet):
    queryset = CastMember.objects.all()
    serializer_class = CastMemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["movie"]
