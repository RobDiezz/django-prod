"""Модуль для определения моделей аутентификации и профиля пользователя."""

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    """Определяет путь для сохранения аватара пользователя."""
    return f"profile/user_{instance.user.pk}/avatars/{filename}"


class Profile(models.Model):
    """Модель профиля пользователя."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=profile_avatar_directory_path, null=True, blank=True)

    def __str__(self):
        """Возвращает строковое представление профиля."""
        return self.user.username

    def get_absolute_url(self):
        return reverse("myauth:user-detail", kwargs={"pk": self.pk})
