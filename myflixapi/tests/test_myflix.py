from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from myflixapi.models import CastMember, CrewMember, Genre, Movie
from myflixapi.tests.factories import GenreFactory, MovieFactory, UserFactory
from myflixapi.views import MovieViewSet

User = get_user_model()
# Create your tests here.


# This is a test case class for testing user registration, login, profile update, and account deletion
class UserTestView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/auth/register/"
        self.login_url = "/auth/login/"
        self.delete_account_url = "/auth/delete_account/"
        self.delete_crewmember_url = "/api/crewmembers/1/"
        self.user = UserFactory.create()
        self.update_profile_url = f"/auth/update_profile/{self.user.id}/"
        self.authenticate()

    def authenticate(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "username",
                "password": "defaultpassword",
            },
        )
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_register(self):
        # register data
        data = {
            "username": "joanna2",
            "email": "asia.jeziorekk++!@gmail.com",
            "first_name": "asia",
            "last_name": "asia",
            "password": "testowe144",
            "password2": "testowe144",
        }
        # send POST request to "/auth/register/"
        response = self.client.post(self.register_url, data)
        # check the response status and data
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(len(mail.outbox), 1)

    def test_login(self):
        # login data
        data = {
            "username": "username",
            "password": "defaultpassword",
        }
        response = self.client.post(self.login_url, data)
        # check the response status and data
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        data = {
            "username": "testuser3",
        }
        response = self.client.patch(self.update_profile_url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(User.objects.get(id=self.user.id).username, "testuser3")

    def test_delete_account(self):
        user_id = self.user.id
        response = self.client.delete(self.delete_account_url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(User.objects.filter(id=user_id)), 0)

    def test_fail_delete_crew_member(self):
        response = self.client.delete(self.delete_crewmember_url)

        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


# This is a test class for testing the functionality of a MovieViewSet in a Django REST API, including
# authentication, retrieving movie details, and searching for movies by title.
class MovieTestView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = MovieViewSet.as_view({"get": "list"})
        self.client = APIClient()
        self.movies_url = "/api/movies/"
        self.login_url = "/auth/login/"
        UserFactory.create()
        self.movie_obj = Movie.objects.create(
            title="test movie", external_movie_id=12345
        )
        self.authenticate()

        MovieFactory.create(genres=(GenreFactory(), GenreFactory()))
        MovieFactory.create_batch(100, genres=(GenreFactory(), GenreFactory()))

    def authenticate(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "username",
                "password": "defaultpassword",
            },
        )
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_get_movies(self):
        response = self.client.get(self.movies_url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(list(response.data.items())[0][1], 102)

    def test_get_movie_details(self):
        response = self.client.get(
            f"{self.movies_url}{self.movie_obj.external_movie_id}/"
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["title"], "test movie")

    def test_unathorized_get_movie_details(self):
        self.client.logout()
        response = self.client.get(
            f"{self.movies_url}{self.movie_obj.external_movie_id}/"
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_movie_by_title(self):
        m3 = MovieFactory(title="Harry Potter")

        response = self.client.get(f"{self.movies_url}?search=harry")

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(list(response.data.items())[0][1], 1)

    def test_filter_movie_by_genre(self):
        g1 = GenreFactory(title="Fantasy")
        m1 = MovieFactory(title="Harry Potter", genres=(g1,))

        response = self.client.get(f"{self.movies_url}?genres={g1.external_genre_id}")

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(list(response.data.items())[0][1], 1)
