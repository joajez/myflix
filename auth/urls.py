from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from auth.views import (ChangePasswordView, DeleteAccountView,
                        MyObtainTokenPairView, RegisterView, UpdateProfileView)

urlpatterns = [
    path("login/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path(
        "change_password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="auth_change_password",
    ),
    path(
        "update_profile/<int:pk>/",
        UpdateProfileView.as_view(),
        name="auth_update_profile",
    ),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path(
        "delete_account/",
        DeleteAccountView.as_view(),
        name="delete_account",
    ),
]
