from django.contrib import admin
from .models import Contact, TeamMember, Service, PortfolioProject, BlogPost, Item


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "created_at")
    search_fields = ("name", "email", "company")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "email", "order")
    search_fields = ("name", "position", "email")
    list_editable = ("order",)
    ordering = ("order", "name")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "expertise", "order", "price_range")
    search_fields = ("title", "expertise")
    list_filter = ("expertise",)
    list_editable = ("order",)
    ordering = ("order", "title")


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "expertise", "featured", "completion_date")
    search_fields = ("title", "client", "expertise", "technologies")
    list_filter = ("expertise", "featured", "completion_date")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "published", "published_date", "created_at")
    search_fields = ("title", "content", "author__username")
    list_filter = ("category", "published", "published_date", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-published_date", "-created_at")


# Keep existing Item for now
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "owner", "created_at")
	search_fields = ("name", "owner__username")
	raw_id_fields = ("owner",)
