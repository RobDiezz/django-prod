"""Модуль форм для приложения интернет-магазина."""

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group
from django.core import validators
from django.utils.translation import gettext_lazy as _, pgettext_lazy

from .models import Product, Order


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=1000000, decimal_places=2)
#     description = forms.CharField(
#         label="Product description",
#         widget=forms.Textarea(attrs={"rows": 5, "cols": "20"}),
#         validators=[
#             validators.RegexValidator(
#                 regex=r"great",
#                 message="Field must contain word 'great'",
#             )
#         ],
#     )


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         exclude = ["created_at", "archived"]
#         # fields = "name", "price", "description", "discount"
#         widgets = {
#             "description": forms.Textarea(attrs={"rows": 5, "cols": 30}),
#         }
#         labels = {"description": "Product description"}


class OrderForm(forms.ModelForm):
    """Форма для создания и редактирования заказов."""

    class Meta:
        """Метаданные формы заказа."""

        model = Order
        # exclude = ["created_at"]
        fields = ["user", "products", "promocode", "delivery_address", "receipt"]
        widgets = {
            "delivery_address": forms.Textarea(attrs={"rows": 3, "cols": 30}),
        }
        labels = {
            "user": _("Customer"),
            "products": _("Products"),
            "promocode": _("Promocode"),
            "delivery_address": _("Delivery address"),
            "receipt": _("Receipt"),
        }
        error_messages = {"promocode": {"max_length": "The promo code is too long."}}


class GroupForm(ModelForm):
    """Форма для создания и редактирования групп пользователей."""

    class Meta:
        """Метаданные формы групп."""

        model = Group
        fields = ["name"]
        labels = {
            "name": pgettext_lazy("group name", "Name"),
        }


class MultipleFileInput(forms.ClearableFileInput):
    """Виджет для загрузки нескольких файлов."""

    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Поле формы для загрузки нескольких файлов."""

    def __init__(self, *args, **kwargs):
        """Инициализирует поле с виджетом для загрузки нескольких файлов."""
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        """Очистка данных перед их сохранением."""
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта."""

    class Meta:
        """Метаданные формы продукта."""

        model = Product
        fields = [
            "name",
            "price",
            "description",
            "discount",
            "preview",
        ]
        labels = {
            "name": pgettext_lazy("product name", "Name"),
            "price": _("Price"),
            "description": _("Description"),
            "discount": _("Discount"),
            "preview": _("Preview"),
        }

    # Устарело
    # images = forms.ImageField(
    #     widget=forms.ClearableFileInput(attrs={"multiple": True}),
    #     required=False,
    # )
    images = MultipleFileField(required=False, label=_("Images"))


class CSVJSONImportForm(forms.Form):
    upload_file = forms.FileField(label=_("File"))
