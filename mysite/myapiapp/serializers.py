"""Модуль для определения сериализаторов в приложении myapiapp."""

from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        """Вложенный класс, содержащий метаданные для сериализатора GroupSerializer."""

        model = Group
        fields = "pk", "name"
