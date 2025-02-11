"""Создание в административной панели полей и опций."""

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .common import save_csv, save_json
from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVJSONImportForm


class OrderInline(admin.TabularInline):
    """Inline для управления продуктами, связанными с заказом."""

    model = Product.orders.through
    extra = 0  # Удаляет три пустых строки в Order product relationships
    verbose_name = _("order")
    verbose_name_plural = _("orders")


class ProductImageInline(admin.StackedInline):
    """Inline для управления изображениями продуктов."""

    model = ProductImage


@admin.action(description="Archived products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    """Помечает выбранные продукты как архивированные."""
    queryset.update(archived=True)


@admin.action(description="Unarchived products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    """Снимает пометку архивирования с выбранных продуктов."""
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    """Административный интерфейс для управления продуктами."""

    change_list_template = "shopapp/shopapp_changelist.html"

    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [OrderInline, ProductImageInline]
    # list_display = "pk", "name", "description", "price", "discount"
    list_display = (
        "pk",
        "name",
        "description_short",
        "price",
        "discount",
        "archived",
    )
    list_display_links = "pk", "name"
    ordering = "name", "pk"
    search_fields = "name", "description"
    fieldsets = [
        (
            None,
            {
                "fields": ("name", "description"),
            },
        ),
        (
            _("Price options"),
            {
                "fields": ("price", "discount"),
                "classes": ("wide", "collapse"),
            },
        ),
        (
            _("Images"),
            {
                "fields": ("preview",),
            },
        ),
        (
            _("Extra options"),
            {
                "fields": ("archived",),
                "classes": ("collapse",),
                "description": _("Extra options. Field 'archives' is for soft delete"),
            },
        ),
    ]

    def description_short(self, obj: Product) -> str:
        """
        Возвращает укороченное описание продукта.

        Если описание меньше 48 символов, возвращает его целиком.
        """
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."

    description_short.short_description = _("Description")

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVJSONImportForm()
            context = {
                "form": form,
                "file_csv": True,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVJSONImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)

        save_csv(
            obj=Product,
            file=form.files["csv_file"].file,
            encoding=request.encoding,
        )
        self.message_user(request, _("Data from %s was imported.") % "CSV")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            ),
        ]
        return new_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["url_import_csv"] = "admin:import_products_csv"
        return super().changelist_view(request=request, extra_context=extra_context)


# admin.site.register(Product, ProductAdmin)


class ProductInline(admin.StackedInline):
    """Inline для управления продуктами, связанными с заказом."""

    model = Order.products.through
    extra = 0
    verbose_name = _("product")
    verbose_name_plural = _("products")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления заказами."""

    change_list_template = "shopapp/shopapp_changelist.html"

    inlines = [
        ProductInline,
    ]
    list_display = (
        "delivery_address",
        "promocode",
        "created_at",
        "user",
    )

    def get_queryset(self, request):
        """Возвращает queryset для отображения в административном интерфейсе."""
        return Order.objects.select_related("user").prefetch_related("products")

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVJSONImportForm()
            context = {
                "form": form,
            }
            if request.path.endswith("-csv/"):
                context["file_csv"] = True
            elif request.path.endswith("-json/"):
                context["file_json"] = True
            return render(request, "admin/csv_form.html", context)

        form = CSVJSONImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)

        uploaded_file = form.files["upload_file"]
        message_base = _("Data from %s was imported.")
        redirect_dir = ".."
        level = messages.SUCCESS

        if uploaded_file.name.endswith(".csv"):
            save_csv(
                obj=Order,
                file=uploaded_file.file,
                encoding=request.encoding,
                key="products",
            )
            message_base %= "CSV"
        elif uploaded_file.name.endswith(".json"):
            save_json(
                obj=Order,
                file=uploaded_file.file,
                encoding=request.encoding,
                key="products",
            )
            message_base %= "JSON"
        else:
            message_base = _("The file must have the extension CSV or JSON")
            level = messages.ERROR
            redirect_dir = "."
        self.message_user(request, message_base, level=level)
        return redirect(redirect_dir)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-orders-csv/",
                self.import_csv,
                name="import_orders_csv",
            ),
            path(
                "import-orders-json/",
                self.import_csv,
                name="import_orders_json",
            ),
        ]
        return new_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["url_import_csv"] = "admin:import_orders_csv"
        extra_context["url_import_json"] = "admin:import_orders_json"
        return super().changelist_view(request=request, extra_context=extra_context)
