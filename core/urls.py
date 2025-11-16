from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),

    # New business pages
    path("contact/", views.contact_view, name="contact"),
    path("team/", views.TeamListView.as_view(), name="team"),
    path("services/", views.services_view, name="services"),
    path("portfolio/", views.PortfolioListView.as_view(), name="portfolio"),
    path("portfolio/<int:project_id>/", views.portfolio_detail_view, name="portfolio_detail"),
    path("blog/", views.BlogListView.as_view(), name="blog"),
    path("blog/<slug:slug>/", views.blog_detail_view, name="blog_detail"),

    # About and legal pages
    path("about/", views.about_view, name="about"),
    path("privacy/", views.privacy_view, name="privacy"),
    path("terms/", views.terms_view, name="terms"),

    # Downloads
    path("brochure/", views.brochure_view, name="brochure"),

    # Legacy Item CRUD (can be removed later)
    path("items/", views.ItemListView.as_view(), name="item_list"),
    path("items/create/", views.ItemCreateView.as_view(), name="item_create"),
    path("items/<int:pk>/", views.ItemDetailView.as_view(), name="item_detail"),
    path("items/<int:pk>/edit/", views.ItemUpdateView.as_view(), name="item_update"),
    path("items/<int:pk>/delete/", views.ItemDeleteView.as_view(), name="item_delete"),
]
