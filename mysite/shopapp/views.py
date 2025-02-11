"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т.д.
"""

import csv
import logging
from timeit import default_timer as timer
from typing import Any, Dict, List, Tuple
from csv import DictWriter

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib.syndication.views import Feed
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from faker import Faker

from .common import save_csv
from .forms import OrderForm, GroupForm, ProductForm
from .models import Order, Product, ProductImage
from .serializers import ProductSerializer, OrderSerializer

log = logging.getLogger(__name__)

fake = Faker("ru_RU")


@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.

    Полный CRUD для сущности товаров.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        "name",
        "description",
    ]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        # print("Hello products list")
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by ID not found"),
        },
    )
    def retrieve(self, *args, **kwargs):
        """Метод возвращает ответ с данными объекта."""
        return super().retrieve(*args, **kwargs)

    @action(methods=["get"], detail=False)
    def downloads_csv(self, request: Request) -> HttpResponse:
        response = HttpResponse(content_type='text/csv')
        file_name = "products-export.csv"
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({field: getattr(product, field) for field in fields})

        return response

    @action(
        methods=["post"],
        detail=False,
        parser_classes=[MultiPartParser],
    )
    def upload_csv(self, request: Request):
        products = save_csv(
            Product,
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    """Класс для административной панели заказов."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        "created_at",
        "delivery_address",
    ]
    filterset_fields = [
        "user",
        "products",
        "promocode",
        "delivery_address",
        "created_at",
    ]
    ordering_fields = [
        "user",
        "created_at",
        "delivery_address",
    ]


class ShopIndexView(View):
    """Класс представления."""

    # @method_decorator(cache_page(60 * 2)) # Можно оставить только тут и убрать из urls.py
    def get(self, request: HttpRequest) -> HttpResponse:
        """Метод по обработке GET-запроса."""
        products: List[Tuple[str, int]] = [
            ("laptop", 1999),
            ("desktop", 2999),
            ("smartphone", 999),
        ]
        text_ru = fake.texts(nb_texts=3)
        context: Dict[str, Any] = {
            "time_running": timer,
            "products": products,
            "items": 1,
            "text": text_ru,
        }
        print("shop index context", context)
        log.debug("Products for shop index: %s", products)
        log.info("Rendering shop index")
        return render(request, "shopapp/shop-index.html", context=context)


class GroupsListView(View):
    """Класс выводит список групп."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Метод по обработке GET-запроса."""
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related("permissions").all(),
        }
        return render(request, "shopapp/groups-list.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Метод по обработке POST-запроса."""
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


# class ProductDetailsView(View):
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         product = get_object_or_404(Product, pk=pk)
#         context = {
#             "product": product,
#         }
#         return render(request, "shopapp/products-details.html", context=context)


# class ProductsListView(TemplateView):
#     template_name = "shopapp/products_list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["products"] = Product.objects.all()
#         return context


class ProductDetailsView(DetailView):
    """Класс выводит детали по каждому товару."""

    template_name = "shopapp/products-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    """Класс позволяет вывести список товаров."""

    template_name = "shopapp/products_list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """Класс по созданию товара."""

    # UserPassesTestMixin можно использовать вместо Permission
    # def test_func(self):
    #     # return self.request.user.groups.filter(name="group_products").exists()
    #     return self.request.user.is_superuser
    permission_required = "shopapp.add_product"

    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    form_class = ProductForm

    # При объявления метода get_absolute_url в классе. Этот метод можно не использовать
    # success_url = reverse_lazy("shopapp:product_list")

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)

    def form_valid(self, form):
        """Метод проверяет, что все данные прошли проверку."""
        form.instance.user = self.request.user
        files = form.cleaned_data["images"]
        for image in files:
            ProductImage.objects.create(product=self.object, image=image)

        return super().form_valid(form)


# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             # name = form.cleaned_data["name"]
#             # price = form.cleaned_data["price"]
#             # description = form.cleaned_data["description"]
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse("shopapp:product_list")
#             return redirect(url)
#     else:
#         form = ProductForm()
#     context = {"form": form}
#
#     return render(request, "shopapp/create-product.html", context=context)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    """Класс позволяет обновить данные товара."""

    def test_func(self):
        """Метод проверяет права доступа пользователя."""
        if self.request.user.is_superuser:
            return True
        create_user = self.request.user == self.get_object().created_by
        perms_user = self.request.user.has_perm("shopapp.change_product")
        return create_user and perms_user

    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm

    # При объявления метода get_absolute_url в классе. Этот метод можно не использовать
    # def get_success_url(self):
    #     """Метод определяет куда перенаправить пользователя после успешной обработки формы."""
    #     return reverse(
    #         "shopapp:product_details",
    #         kwargs={"pk": self.object.pk},
    #     )

    def form_valid(self, form):
        """Метод проверяет, что все данные прошли проверку."""
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(product=self.object, image=image)

        return response


class ProductDeleteView(UserPassesTestMixin, DeleteView):
    """Класс для удаления товара."""

    def test_func(self):
        """Проверка прав пользователя, для возможности удалить товар."""
        if self.request.user.is_superuser:
            return True
        create_user = self.request.user == self.get_object().created_by
        perms_user = self.request.user.has_perm("shopapp.delete_product")
        return create_user and perms_user

    model = Product
    success_url = reverse_lazy("shopapp:product_list")

    def form_valid(self, form):
        """Проверка валидности формы."""
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    """Класс выводит список заказов."""

    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderDetailView(PermissionRequiredMixin, DetailView):
    """Класс выводит детали заказа."""

    permission_required = "shopapp.view_order"
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderCreateView(CreateView):
    """Класс позволяет создать новый заказ."""

    model = Order
    form_class = OrderForm
    template_name = "shopapp/create-order.html"
    # При объявления метода get_absolute_url в классе. Этот метод можно не использовать
    # success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    """Класс позволяет изменять заказ."""

    model = Order
    form_class = OrderForm
    template_name_suffix = "_update_form"

    # При объявления метода get_absolute_url в классе. Этот метод можно не использовать
    # def get_success_url(self):
    #     """При успешном запросе url перенаправляем на детали заказа."""
    #     return reverse(
    #         "shopapp:order_details",
    #         kwargs={"pk": self.object.pk},
    #     )


class OrderDeleteView(DeleteView):
    """Класс показывает детали заказа."""

    model = Order
    success_url = reverse_lazy("shopapp:orders_list")

    def form_valid(self, form):
        """Проверка валидности формы."""
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


# def create_order(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse("shopapp:orders_list")
#             return redirect(url)
#     else:
#         form = OrderForm()
#
#     context = {"form": form}
#     return render(request, "shopapp/create-order.html", context=context)


class ProductDataExportView(View):
    """Класс экспорта товаров."""

    def get(self, request: HttpRequest) -> JsonResponse:
        """Метод выводит все товары."""
        cache_key = "myauth/cookie/get"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archived": product.archived,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)
        elem = products_data[0]
        name = elem["name"]
        print("name", name)
        return JsonResponse({"products": products_data})


class OrdersExportView(UserPassesTestMixin, View):
    """Класс экспорт заказов."""

    def test_func(self):
        """Проверка прав пользователя."""
        return self.request.user.is_staff

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """Метод выводит все заказы."""
        orders = Order.objects.prefetch_related("products").all()

        orders_data = [
            {
                "id": order.id,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user_id": order.user.id,
                "products": [prod.pk for prod in order.products.all()],
                # "products": list(order.products.values_list("id", flat=True)),
            }
            for order in orders
        ]

        return JsonResponse({"orders": orders_data})


class LatestProductsFeed(Feed):
    title = _("Product list (latest)")
    description = _("Updates on changes and addition products")
    link = reverse_lazy("shopapp:product_list")

    def items(self):
        return Product.objects.filter(archived=False).order_by("-created_at")

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:5] + ("" if len(item.description) < 5 else "...")


class UserOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "shopapp/user_orders.html"
    context_object_name = "user_orders"

    @property
    def owner(self):
        if not hasattr(self, "_owner"):
            user_id = self.kwargs.get("user_id")
            self._owner = get_object_or_404(User, pk=user_id)
        return self._owner

    def get_queryset(self):
        return Order.objects.filter(user=self.owner).select_related("user").prefetch_related("products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owner"] = self.owner
        return context


class UserOrdersExportView(View):
    def owner(self, user_id):
        user_id = self.kwargs.get("user_id")
        return get_object_or_404(User, pk=user_id)

    def get(self, request: HttpRequest, user_id) -> JsonResponse:
        """Метод выводит все заказы."""
        user = self.owner(user_id)
        cache_key = user.username + str(user.pk)
        orders_data = cache.get(cache_key)
        if orders_data is None:
            orders = (
                Order.objects.filter(user=user)
                .select_related("user")
                .prefetch_related(
                    Prefetch("products", queryset=Product.objects.only("pk").order_by("pk")),
                )
                .order_by("pk")
            )
            user_orders_key = user.username + "_orders"
            orders_data = {
                user_orders_key: [
                    {
                        "id": order.id,
                        "created_at": order.created_at,
                        "delivery_address": order.delivery_address,
                        "promocode": order.promocode,
                        "user_id": order.user.id,
                        "products": [prod.pk for prod in order.products.all()],
                        "receipt": order.receipt.path if order.receipt else None,
                        # "products": list(order.products.values_list("id", flat=True)),
                    }
                    for order in orders
                ],
            }
            cache.set(cache_key, orders_data, 300)
            print("Create cache", cache_key)
        print("Go back cache")
        return JsonResponse({"orders": orders_data})
