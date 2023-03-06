from django.conf import settings
import requests
from .models import Movie, Genre


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
    print("______________________________")
    for movie in popular_movies["results"]:
        print(movie)
        genres = Genre.objects.filter(genre_id__in=movie["genre_ids"])
        movie_obj, created = Movie.objects.get_or_create(
            movie_id=movie["id"],
            title=movie["original_title"],
            language=movie["original_language"],
            release_date=movie["release_date"],
        )
        for g in genres:
            movie_obj.genre.add(g)


# from myflixapi.utils import fill_db_with_genres; fill_db_with_genres();
# from myflixapi.utils import fill_db_with_popular_movies; fill_db_with_popular_movies();
# from myflixapi.utils import get_genres_from_tmd; get_genres_from_tmd();
# https://api.themoviedb.org/3/movie/550?api_key=b48f123dcf12d55315a7b21a43f728ac
