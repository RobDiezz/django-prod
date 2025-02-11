from string import ascii_letters
from random import choices

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product, Order
from shopapp.utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(4, 3)
        self.assertEqual(result, 7)


class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

        permissions = Permission.objects.get(codename="add_product")
        self.user.user_permissions.add(permissions)

    def test_create_product(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "A good table",
                "discount": "10",
            },
        )
        self.assertRedirects(response, reverse("shopapp:product_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best product")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):
    fixtures = [
        "auth_group.json",
        "auth_user.json",
        "products-fixture.json",
    ]

    def test_products(self):
        response = self.client.get(reverse("shopapp:product_list"))
        # 1 variant
        # for product in Product.objects.filter(archived=False).all():
        #     self.assertContains(response, product.name)

        # 2 variant
        # product = Product.objects.filter(archived=False).all()
        # product_ = response.context["products"]
        # for p, p_ in zip(product, product_):
        #     self.assertEqual(p.pk, p_.pk)

        # 3 variant
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=[p.pk for p in response.context["products"]],
            transform=lambda p: p.pk,
            ordered=False,
        )

        self.assertTemplateUsed(response, "shopapp/products_list.html")


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        # expected_redirect_url = f"{settings.LOGIN_URL}?next=/shop/orders/"
        # self.assertRedirects(response, expected_redirect_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        "auth_group.json",
        "auth_user.json",
        "products-fixture.json",
    ]

    def test_get_products_view(self):
        response = self.client.get(reverse("shopapp:products_export"))
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data,
        )


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        permissions = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(permissions)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.product = Product.objects.create(name="Product test", price="123.45")

        self.order = Order.objects.create(
            user=self.user,
            promocode="Test promocode",
            delivery_address="Test delivery address",
        )

        self.order.products.set([self.product])

    def tearDown(self):
        self.order.delete()
        self.product.delete()

    def test_order_detail_view(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context["order"].pk, self.order.pk)


class OrdersExportViewTestCase(TestCase):
    fixtures = [
        "auth_group.json",
        "auth_user.json",
        "products-fixture.json",
        "orders-fixture.json",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.staff_user = User.objects.create_user(
            username="staffuser",
            password="testpassword",
            is_staff=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.staff_user.delete()

    def setUp(self):
        self.client.force_login(self.staff_user)

    def test_orders_export_view(self):
        response = self.client.get(reverse("shopapp:orders_export"))

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {
                "orders": [
                    {
                        "id": order.id,
                        "delivery_address": order.delivery_address,
                        "promocode": order.promocode,
                        "user_id": order.user.id,
                        "products": [prod.pk for prod in order.products.all()],
                        # "products": list(order.products.values_list("id", flat=True)),
                    }
                    for order in Order.objects.all()
                ]
            },
        )
