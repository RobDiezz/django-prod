"""Модуль управления для создания новых заказов в интернет-магазине."""

from typing import Any

from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandError, CommandParser

from shopapp.models import Order


class Command(BaseCommand):
    """Создает новый заказ."""

    def add_arguments(self, parser: CommandParser) -> None:
        """Добавляет аргументы для команды."""
        parser.add_argument("--username", type=str, help="Create user name")
        parser.add_argument("--delivery_address", type=str, help="Delivery address")
        parser.add_argument("--promocode", type=str, help="Promocode")

    def handle(self, *args: Any, **options: Any):
        """Обрабатывает выполнение команды создания заказа."""
        username: str = options["username"]
        delivery_address: str = options["delivery_address"]
        promocode: str = options["promocode"]

        if not username:
            self.stdout.write(self.style.ERROR("No such user"))
            return

        self.stdout.write("Create order")
        try:
            user: User = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"User {username} does not exist")

        order, created = Order.objects.get_or_create(delivery_address=delivery_address, promocode=promocode, user=user)

        if created:
            action: str = "Created"
        else:
            action: str = "Extracts"

        self.stdout.write(f"Order {order.id} {action}")
