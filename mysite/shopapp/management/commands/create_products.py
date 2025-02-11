"""
Модуль управления для создания продуктов в базе данных.

Этот модуль содержит команду для создания продуктов в интернет-магазине.
"""

from typing import Dict, Tuple

from django.core.management import BaseCommand, CommandError
from django.core.management.base import CommandParser

from shopapp.models import Product


class Command(BaseCommand):
    """Создает продукты в базе данных."""

    def add_arguments(self, parser: CommandParser) -> None:
        """Добавляет аргументы для команды."""
        parser.add_argument("--quantity", type=int, help="Quantity of products")

    def handle(self, *args, **options) -> None:
        """Обрабатывает выполнение команды создания продуктов."""
        quantity = options["quantity"]
        if not quantity or quantity > 3:
            self.stdout.write(self.style.ERROR("Quantity of products cannot be empty, be from 1 to 3"))
            return
        self.stdout.write("Create products")

        product_names: Tuple[Dict[str, str | int], ...] = (
            {
                "name": "Laptop",
                "description": "MacBook Pro 16 Core 10",
                "price": 1999,
                "discount": 10,
            },
            {
                "name": "Desktop",
                "description": "MSI ПК MSI MAG Infinite S3",
                "price": 899,
                "discount": 10,
            },
            {
                "name": "Smartphone",
                "description": "iPhone 14 ProMax 512GB",
                "price": 999,
                "discount": 15,
            },
        )

        for i in range(quantity):
            product, created = Product.objects.get_or_create(**product_names[i])
            if created:
                action: str = "Created"
            else:
                action: str = "Extracts"
            self.stdout.write(f"{action} '{product.name}' product")

        self.stdout.write(self.style.SUCCESS(f"Created products {action.lower()}"))
