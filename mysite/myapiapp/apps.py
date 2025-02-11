"""Модуль конфигурации приложения myapiapp."""

from django.apps import AppConfig


class MyapiappConfig(AppConfig):
    """Конфигурация приложения myapiapp."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "myapiapp"
