"""Модуль для определения форм аутентификации и профиля пользователя."""

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Profile


class ProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя."""

    class Meta:
        """Вложенный класс, содержащий метаданные для формы ProfileForm."""

        model = Profile
        fields = ["bio", "agreement_accepted", "avatar"]  # Укажите поля из Profile
        labels = {
            "bio": _("Biography"),
            "agreement_accepted": _("Agreement"),
            "avatar": "",
        }


class UserForm(forms.ModelForm):
    """Форма для редактирования информации о пользователе."""

    class Meta:
        """Вложенный класс, содержащий метаданные для формы UserForm."""

        model = User
        fields = ["first_name", "last_name", "email"]  # Укажите поля из User
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
            "email": _("E-mail"),
        }


class AvatarUpdateForm(forms.ModelForm):
    """Форма для обновления аватара пользователя."""

    class Meta:
        """Вложенный класс, содержащий метаданные для формы AvatarUpdateForm."""

        model = Profile
        fields = ["avatar"]
        labels = {"avatar": _("Change avatar")}
