"""Модуль конфигурации приложения для аутентификации пользователей."""

from django.apps import AppConfig


class MyauthConfig(AppConfig):
    """Конфигурация приложения 'myauth'."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "myauth"
