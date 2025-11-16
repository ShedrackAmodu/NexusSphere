from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import PortfolioProject, Service, TeamMember, BlogPost


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['core:index', 'core:contact', 'core:services', 'core:portfolio', 'core:team', 'core:blog']

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Service.objects.all()


class PortfolioSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return PortfolioProject.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class TeamSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return TeamMember.objects.all()


class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.created_at
