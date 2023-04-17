from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genre(models.Model):
    external_genre_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


# Create your models here.
class Movie(models.Model):
    external_movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=120)
    language = models.CharField(max_length=20)
    genres = models.ManyToManyField(Genre)
    release_date = models.DateField(null=True)

    def __str__(self):
        return self.title


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie, related_name="movies")


class CrewMember(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=120)
    department = models.CharField(max_length=120, null=True)
    job = models.CharField(max_length=120, null=True)


class CastMember(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    character_name = models.CharField(max_length=120, null=True)
