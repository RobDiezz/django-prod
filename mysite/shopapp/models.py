"""
Модуль моделей для приложения интернет-магазина.

Этот модуль содержит определения моделей, используемых в приложении,
включая модели для продуктов, изображений продуктов и заказов.
"""

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, pgettext_lazy


def product_preview_directory_path(instance: "Product", filename: str) -> str:
    """Генерирует путь к директории для предварительного просмотра продукта."""
    return f"products/product_{instance.pk}/preview/{filename}"


class Product(models.Model):
    """
    Модель Product представляет товар, который можно продавать в интернет-магазине.

    Заказы тут: :model:`shopapp.Order`
    """

    name = models.CharField(max_length=100, verbose_name=pgettext_lazy("product name", "name"), db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=_("price"))
    description = models.TextField(null=False, blank=True, verbose_name=_("description"), db_index=True)
    discount = models.PositiveSmallIntegerField(default=0, verbose_name=_("discount"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    archived = models.BooleanField(default=False, verbose_name=_("archived"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_product",
        null=True,
        verbose_name=_("created by"),
    )
    preview = models.ImageField(
        null=True,
        blank=True,
        upload_to=product_preview_directory_path,
        verbose_name=_("preview"),
    )

    # @property
    # def description_short(self)-> str:
    #     if len(self.description) < 0:
    #         return self.description
    #     return self.description[:48] + "..."

    class Meta:
        """Мета данные модели продукта."""

        ordering = ["name", "price"]
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self) -> str:
        """Возвращает строковое представление продукта с его именем и ценой."""
        return _("Product %(name)s for %(price)d $") % {
            "name": self.name,
            "price": self.price,
        }

    def get_absolute_url(self) -> str:
        return reverse("shopapp:product_details", kwargs={"pk": self.pk})


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    """Генерирует путь к директории для изображений продукта."""
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    """
    Модель для хранения изображений продуктов.

    Эта модель связывает изображения с продуктами в интернет-магазине.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("product"),
    )
    image = models.ImageField(upload_to=product_images_directory_path, verbose_name=_("image"))
    description = models.CharField(max_length=200, null=False, blank=True, verbose_name=_("description"))

    class Meta:
        """Метаданные модели продукта."""

        verbose_name = _("product image")
        verbose_name_plural = _("product images")

    def __str__(self) -> str:
        """Возвращает строковое представление изображения продукта."""
        return f"Image for {self.product}"


class Order(models.Model):
    """
    Модель Order представляет заказы, которые оформлены в интернет-магазине.

    Товары тут: :model: `shopapp.Product`
    """

    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("user"))
    products = models.ManyToManyField(
        Product,
        related_name="orders",
        verbose_name=_("products"),
    )
    promocode = models.CharField(max_length=20, null=False, blank=True, verbose_name=_("promocode"))
    delivery_address = models.TextField(verbose_name=_("delivery address"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    receipt = models.FileField(null=True, blank=True, upload_to="orders/receipts/", verbose_name=_("receipt"))

    class Meta:
        """Метаданные модели заказа."""

        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self) -> str:
        """Возвращает строковое представление заказа с его уникальным идентификатором."""
        return _("Order # %d") % (self.pk,)

    def get_absolute_url(self) -> str:
        return reverse("shopapp:order_details", kwargs={"pk": self.pk})
