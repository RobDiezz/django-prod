from django.contrib.sitemaps import Sitemap

from .models import Profile


class ProfileSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.3

    def items(self):
        return Profile.objects.order_by('-user__date_joined')

    def lastmod(self, obj: Profile):
        return obj.user.date_joined
