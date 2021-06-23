from django.contrib import sitemaps
from django.urls import reverse
from homepage.models import Dev


class StaticViewSitemap(sitemaps.Sitemap):
    # priority = 0.5
    # changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['homepage:dev', 'homepage:about', 'homepage:popnews', 'homepage:devall', 'homepage:devlist',
                'homepage:background', 'users:register', 'users:profile', 'users:login', 'users:logout',
                'users:password_reset_confirm', 'users:password_reset_complete', 'users:password_reset']

    def priority(self, item):
        return {'homepage:dev': 1.0, 'homepage:about': 0.5, 'homepage:popnews': 1.0, 'homepage:devall': 1.0,
                'homepage:devlist': 0.8, 'homepage:background':0.5, 'users:register': 0.5, 'users:profile': 0.5,
                'users:login': 0.5, 'users:logout': 0.5, 'users:password_reset_confirm': 0.5,
                'users:password_reset_complete': 0.5, 'users:password_reset': 0.5}[item]

    def changefreq(self, item):
        return {'homepage:dev': 'hourly', 'homepage:about': 'yearly', 'homepage:popnews': 'hourly',
                'homepage:devall': 'hourly', 'homepage:devlist': 'monthly', 'homepage:background': 'yearly',
                'users:register': 'yearly', 'users:profile': 'yearly', 'users:login': 'yearly',
                'users:logout': 'yearly', 'users:password_reset_confirm': 'yearly',
                'users:password_reset_complete': 'yearly', 'users:password_reset': 'yearly'}[item]

    def location(self, item):
        return reverse(item)


class DevSitemap(sitemaps.Sitemap):
    changefreq = "hourly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Dev.objects.all()