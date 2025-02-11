import random
from typing import Sequence

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Order, Product


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create new order with products")
        user = User.objects.get(username="admin")
        # products = Product.objects.defer("description", "price", "created_at").all()
        # products = Product.objects.only("id", "name").all()
        idx_product = list(Product.objects.values_list("id", flat=True))
        idx_random = random.choices(idx_product, k=3)
        product_random = Product.objects.filter(id__in=idx_random)
        order, created = Order.objects.get_or_create(
            delivery_address="ul Vavilova d 11",
            promocode="SALE",
            user=user,
        )
        for product in product_random:
            order.products.add(product)
        order.save()
        self.stdout.write(f"Order created {order}")
