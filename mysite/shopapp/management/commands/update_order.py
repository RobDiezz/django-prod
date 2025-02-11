"""Модуль управления для обновления заказов в интернет-магазине."""

from typing import List

from django.core.management import BaseCommand

from shopapp.models import Order, Product


class Command(BaseCommand):
    """Команда для обновления заказа, добавляя все доступные продукты."""

    def handle(self, *args, **options):
        """
        Обрабатывает выполнение команды обновления заказа.

        Эта функция ищет первый заказ и добавляет к нему все доступные продукты.
        Если заказ не найден, выводит сообщение об ошибке.
        """
        order: Order = Order.objects.first()
        if not order:
            self.stdout.write(self.style.ERROR("No order found."))
            return

        products: List[Product] = Product.objects.all()
        for product in products:
            order.products.add(product)

        order.save()

        self.stdout.write(self.style.SUCCESS(f"Order updated {order.products.all()} to order {order}"))
