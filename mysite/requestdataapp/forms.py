"""Модуль для определения форм в приложении requestdataapp."""

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserBioForm(forms.Form):
    """Форма для ввода биографической информации пользователя."""

    name = forms.CharField(max_length=100)
    age = forms.IntegerField(label="Your age", min_value=1, max_value=100)
    bio = forms.CharField(label="Biography", widget=forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile) -> None:
    """
    Валидирует имя загружаемого файла.

    Проверяет, содержит ли имя файла слово 'virus'. Если да, то вызывает
    исключение ValidationError.
    """
    if file.name and "virus" in file.name:
        raise ValidationError("file name should not contain 'virus'")


class UploadFileForm(forms.Form):
    """Форма для загрузки файлов с валидацией имени файла."""

    file = forms.FileField(validators=[validate_file_name])
