from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import CrewMember, Genre, Movie, CrewMember, CastMember

User = get_user_model()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["title", "language", "genres", "release_date"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = [
            "name",
            "department",
            "job",
        ]


class CastMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastMember
        fields = [
            "name",
            "character_name",
        ]
