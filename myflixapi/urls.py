from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"movies", views.MovieViewSet, basename="movies")
router.register(r"genre", views.GenreViewSet, basename="genre")
