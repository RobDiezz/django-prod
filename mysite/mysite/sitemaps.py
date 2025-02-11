from blogapp.sitemap import BlogSitemap
from shopapp.sitemap import ShopSitemap
from myauth.sitemap import ProfileSitemap

sitemaps = {
    'blog': BlogSitemap,
    'shop': ShopSitemap,
    'auth': ProfileSitemap,
}
