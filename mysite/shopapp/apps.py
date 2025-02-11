"""Конфигурация приложения магазина для управления настройками и метаданными."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShopappConfig(AppConfig):
    """Конфигурация приложения для магазина."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "shopapp"
    verbose_name = _("shopapp")
