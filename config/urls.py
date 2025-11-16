"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.http import HttpResponse
from core.sitemaps import StaticViewSitemap, ServiceSitemap, PortfolioSitemap, TeamSitemap, BlogSitemap

# Simple robots.txt view
def robots_txt(request):
    content = """User-agent: *
Allow: /

# Block access to sensitive areas
Disallow: /admin/
Disallow: /api/

# Allow all search engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Slurp
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: Baiduspider
Allow: /

User-agent: YandexBot
Allow: /

# Sitemap
Sitemap: https://nexusspheresolutions.com/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'portfolio': PortfolioSitemap,
    'team': TeamSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt),
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("core.urls_accounts")),
    path("api/", include(("core.api.urls", "core.api"), namespace="api")),
]
