from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from blogapp.models import Article


class ArticleListView(ListView):
    context_object_name = "articles"
    queryset = (
        Article.objects.filter(pub_date__isnull=False)
        .only("title", "pub_date", "author", "category", "tags")
        .select_related("author", "category")
        .prefetch_related("tags")
        .order_by("-pub_date")
    )


class ArticleDetailView(DetailView):
    queryset = Article.objects.only("title", "pub_date", "author", "content").select_related("author")
    context_object_name = "article"


class LatestArticlesFeed(Feed):
    title = _("Blog Articles (latest)")
    description = _("Updates on changes and addition blog articles")
    link = reverse_lazy("blogapp:article")

    def items(self):
        return Article.objects.filter(pub_date__isnull=False).order_by("-pub_date")[:5]

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:20] + ("" if len(item.content) < 20 else "...")
