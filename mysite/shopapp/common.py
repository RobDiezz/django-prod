import json
from csv import DictReader
from io import TextIOWrapper

from django.contrib.auth.models import User

from .models import Product, Order


def filter_dict(row, key):
    if key is None:
        return row

    dict_orders = {}

    for k, v in row.items():
        if k == "user":
            dict_orders[k] = User.objects.get(username=v)
        elif k != key:
            dict_orders[k] = v

    return dict_orders


def save_csv(obj, file, encoding, key=None):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)
    rows = list(reader)

    objects_list: list[Product | Order] = [obj(**filter_dict(row, key)) for row in rows]
    obj.objects.bulk_create(objects_list)

    if isinstance(obj, type(Order)):
        for idx, row in enumerate(rows):
            if row[key]:
                product = Product.objects.filter(name__in=[prod.strip() for prod in row[key].split(",")])
                objects_list[idx].products.add(*product)

    return objects_list


def save_json(obj: Product | Order, file, encoding, key=None) -> None:
    json_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    data_json: dict[str, dict[str, str | list[str]]] = json.load(json_file)
    for data in data_json.values():
        filtered_dict = filter_dict(data, key)
        created_object = obj.objects.create(**filtered_dict)

        if isinstance(obj, type(Order)):
            products_list = [Product.objects.get(name=name) for name in data[key]]
            created_object.products.add(*products_list)
