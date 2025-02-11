"""Этот модуль содержит сериализаторы для моделей приложения shopapp."""

from rest_framework import serializers

from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    """Cериализатор для модели Product."""

    class Meta:
        """Метаданные для сериализатора Product."""

        model = Product
        fields = (
            "pk",
            "name",
            "description",
            "price",
            "discount",
            "created_at",
            "archived",
            "preview",
        )


class OrderSerializer(serializers.ModelSerializer):
    """Cериализатор для модели Order."""

    class Meta:
        """Метаданные для сериализатора Order."""

        model = Order
        fields = (
            "pk",
            "user",
            "products",
            "promocode",
            "delivery_address",
            "created_at",
            "receipt",
        )
