from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"movies", views.MovieViewSet, basename="movies")
router.register(r"genre", views.GenreViewSet, basename="genre")
router.register(r"crewmembers", views.CrewMemberViewSet, basename="crewmembers")
router.register(r"castmembers", views.CastMemberViewSet, basename="castmembers")
