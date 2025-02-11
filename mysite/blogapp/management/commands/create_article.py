from datetime import datetime

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from ...models import Author, Category, Tag, Article


class Command(BaseCommand):
    help = "Add an author"

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        self.stdout.write("Create new author")
        authors_info = ["Chuck Arnold", "Chuck Arnold is an senior entertainment writer at the New York Post."]
        author, created = Author.objects.get_or_create(name=authors_info[0], bio=authors_info[1])

        category_info = "Show business"
        category, created = Category.objects.get_or_create(
            name=category_info,
        )

        tags_info = ["bands", "albums", "musicians"]
        tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_info]

        article_info = {
            "title": "Joey Fatone on a possible *NSYNC reunion: ‘S—t or get off the pot’",
            "content": "With the 25th anniversary of *NSYNC’s blockbuster album "
            "“No Strings Attached” this year, Joey Fatone said that it’s time for "
            "“that moment of the five of us sitting down going",
            "pub_date": "2025-01-17 15:20:00",
            "author": author,
            "category": category,
        }
        article, created = Article.objects.get_or_create(**article_info)
        article.tags.add(*tags)
        article.save()
        self.stdout.write(f"Create article #{article.pk}")
