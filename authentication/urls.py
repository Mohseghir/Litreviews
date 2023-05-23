from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.urls import path

from authentication.views import signup_page


urlpatterns = [
    path(
        "",
        LoginView.as_view(
            template_name="authentication/index.html",
            redirect_authenticated_user=True
        ),
        name="index",
    ),
    path(
        "login/",
        LoginView.as_view(
            template_name="authentication/login.html",
            redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "change-password/",
        PasswordChangeView.as_view(
            template_name="authentication/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "change-password-done/",
        PasswordChangeDoneView.as_view(
            template_name="authentication/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "signup/",
        signup_page,
        name="signup",
    ),
]


