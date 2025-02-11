from django.db import models
from django.urls import reverse
from django.utils.translation import pgettext_lazy, gettext_lazy as _


class Author(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=pgettext_lazy("author name", "name"),
        db_index=True,
    )
    bio = models.TextField(
        blank=True,
        verbose_name=_("biography"),
    )

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")

    def __str__(self):
        return _("Author id %(pk)d name %(name)s") % {'pk': self.pk, 'name': self.name}


class Category(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name=pgettext_lazy("category name", "name"),
        db_index=True,
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return _("Category id %(pk)d name %(name)s") % {'pk': self.pk, 'name': self.name}


class Tag(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name=pgettext_lazy("tag name", "name"),
        db_index=True,
    )

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        return _("Tag id %(pk)d name %(name)s") % {'pk': self.pk, 'name': self.name}


class Article(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_("title"),
        db_index=True,
    )
    content = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("content"),
    )
    pub_date = models.DateTimeField(verbose_name=_("publication date"))
    author = models.ForeignKey(
        Author,
        related_name="article_author",
        on_delete=models.CASCADE,
        verbose_name=_("author id"),
    )
    category = models.ForeignKey(
        Category,
        related_name="article_category",
        on_delete=models.CASCADE,
        verbose_name=_("category id"),
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="article_tags",
        verbose_name=_("tags"),
    )

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")

    def __str__(self) -> str:
        return _("Article id %(pk)d author %(author)s") % {'pk': self.pk, 'author': self.author}

    def get_absolute_url(self) -> str:
        return reverse("blogapp:article_details", kwargs={"pk": self.pk})
