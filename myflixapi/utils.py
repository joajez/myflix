import json

import requests
from django.conf import settings

from .models import CrewMember, Genre, Movie, CrewMember, CastMember


def get_movie_data(movie_id):
    """Returns movie data from the TMDB API"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.MOVIE_API_KEY}"
    response = requests.get(url)
    return response.json()


def get_movie_image_url(movie_id):
    """Returns movie image url from the TMDB API"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={settings.MOVIE_API_KEY}"
    response = requests.get(url)
    return response.json()


def get_popular_movies_from_tmd():
    """Returns a list of movies from the TMDB API"""
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={settings.MOVIE_API_KEY}"
    response = requests.get(url)
    return response.json()


def get_crew_for_movie(ext_movie_id):
    """Returns crew for movie"""
    url = f"https://api.themoviedb.org/3/movie/{ext_movie_id}/credits?api_key={settings.MOVIE_API_KEY}"
    response = requests.get(url)
    return response.json()


def get_genres_from_tmd():
    """Returns a list of genres from the TMDB API"""
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={settings.MOVIE_API_KEY}"
    response = requests.get(url)
    return response.json()


def fill_db_with_genres():
    genres = get_genres_from_tmd()
    for genre in genres["genres"]:
        Genre.objects.create(
            genre_id=genre["id"],
            title=genre["name"],
        )


def fill_db_with_popular_movies():
    popular_movies = get_popular_movies_from_tmd()
    # CrewMember.objects.all().delete()

    for movie in popular_movies["results"]:
        print("______________________________")
        print(movie)
        genres = Genre.objects.filter(external_genre_id__in=movie["genre_ids"])

        movie_obj, created = Movie.objects.get_or_create(
            external_movie_id=movie["id"],
        )
        if created:
            movie_obj.title = movie["original_title"]
            movie_obj.language = movie["original_language"]
            movie_obj.release_date = movie["release_date"]

            for g in genres:
                movie_obj.genre.add(g)
            movie_obj.save()
        crew = get_crew_for_movie(movie_obj.external_movie_id)
        print(crew.keys())
        for c in crew["crew"]:
            CrewMember.objects.get_or_create(
                movie=movie_obj,
                name=c["name"],
                department=c["department"],
                job=c.get("job"),
            )
        for c in crew["cast"]:
            CastMember.objects.get_or_create(
                name=c["name"],
                movie=movie_obj,
                character_name=c.get("character"),
            )


# get crew members for movies
# https://api.themoviedb.org/3/movie/550/credits?api_key=b48f123dcf12d55315a7b21a43f728ac

# from myflixapi.utils import fill_db_with_genres; fill_db_with_genres();
# from myflixapi.utils import fill_db_with_popular_movies; fill_db_with_popular_movies();
# from myflixapi.utils import get_genres_from_tmd; get_genres_from_tmd();
# https://api.themoviedb.org/3/movie/550?api_key=b48f123dcf12d55315a7b21a43f728ac
