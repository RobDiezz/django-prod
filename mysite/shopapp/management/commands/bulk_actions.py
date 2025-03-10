from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")

        result = Product.objects.filter(
            name__contains="Smartphone",
        ).update(discount=10)

        print(result)

        # info = [
        #     ("Smartphone1", 199),
        #     ("Smartphone2", 299),
        #     ("Smartphone3", 399),
        # ]
        # proucts = [Product(name=name, price=price) for name, price in info]
        #
        # result = Product.objects.bulk_create(proucts)
        #
        # for obj in result:
        #     print(obj)

        self.stdout.write("Done")
