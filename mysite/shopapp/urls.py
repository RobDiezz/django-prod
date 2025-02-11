"""Этот модуль определяет маршруты URL для приложения shopapp."""

from django.urls import path, include
from django.views.decorators.cache import cache_page

from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailsView,
    ProductsListView,
    OrdersListView,
    OrderDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    ProductDataExportView,
    OrdersExportView,
    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed,
    UserOrdersListView,
    UserOrdersExportView,
)

app_name = "shopapp"

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    # path("", cache_page(2 * 3)(ShopIndexView.as_view()), name="shop_index"), # Кэширование
    # это страницы с временем хранения кэша 6сек (2сек * 3).
    path("", ShopIndexView.as_view(), name="shop_index"),
    path("api/", include(router.urls)),
    path("groups/", GroupsListView.as_view(), name="group_list"),
    path("products/", ProductsListView.as_view(), name="product_list"),
    path("products/export/", ProductDataExportView.as_view(), name="products_export"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/latest/feed/", LatestProductsFeed(), name="product_feed"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/export/", OrdersExportView.as_view(), name="orders_export"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user_orders_list"),
    path("users/<int:user_id>/orders/export/", UserOrdersExportView.as_view(), name="user_orders_export"),
]
