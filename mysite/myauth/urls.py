"""
Модуль для определения маршрутов URL приложения аутентификации.

Этот файл содержит все URL-шаблоны, связанные с аутентификацией пользователей,
включая регистрацию, вход, выход и управление профилем.
"""

from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    login_view,
    MyLogoutView,
    MyAboutView,
    RegisterView,
    ProfileUpdateView,
    FooBarView,
    UserListView,
    UserDetailView,
    HelloView,
)

app_name = "myauth"

urlpatterns = [
    path("login/", login_view, name="login"),
    # path(
    #     "login/",
    #     LoginView.as_view(
    #         template_name="myauth/login.html",
    #         redirect_authenticated_user=True,
    #     ),
    #     name="login",
    # ),
    # path("login/", LoginView.as_view(), name="login"),
    path("hello/", HelloView.as_view(), name="hello"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    # path("logout/", login_view, name="logout"),
    path("about-me/<int:pk>/", MyAboutView.as_view(), name="about-me"),
    path("about-me/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>", UserDetailView.as_view(), name="user-detail"),
    path("register/", RegisterView.as_view(), name="register"),
    path("cookie/get/", get_cookie_view, name="get_cookie"),
    path("cookie/set/", set_cookie_view, name="set_cookie"),
    path("session/set/", set_session_view, name="set_session"),
    path("session/get/", get_session_view, name="get_session"),
    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
]
