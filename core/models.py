from django.conf import settings
from django.db import models


# Contact model for lead capture
class Contact(models.Model):
    """Model for storing contact form submissions."""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    company = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


# Team model for member profiles
class TeamMember(models.Model):
    """Model for team member profiles."""
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)  # for ordering

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


# Service model for service offerings
class Service(models.Model):
    """Model for service offerings."""
    EXPERTISE_CHOICES = [
        ('web_apps', 'Web Applications'),
        ('enterprise_saas', 'Learning Management System'),
        ('mobile_apps', 'Mobile Applications'),
        ('geoscience', 'Geoscience Platforms'),
        ('school_mgmt', 'School Management Systems'),
        ('crm', 'CRM Solutions'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    expertise = models.CharField(max_length=20, choices=EXPERTISE_CHOICES)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    features = models.JSONField(default=list, help_text="List of key features")
    price_range = models.CharField(max_length=50, blank=True, help_text="e.g. $10k-$50k")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


# Portfolio model for project showcase
class PortfolioProject(models.Model):
    """Model for portfolio projects."""
    EXPERTISE_CHOICES = [
        ('web_apps', 'Web Applications'),
        ('enterprise_saas', 'Learning Management System'),
        ('mobile_apps', 'Mobile Applications'),
        ('geoscience', 'Geoscience Platforms'),
        ('school_mgmt', 'School Management Systems'),
        ('crm', 'CRM Solutions'),
    ]

    title = models.CharField(max_length=200)
    client = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    expertise = models.CharField(max_length=20, choices=EXPERTISE_CHOICES)
    technologies = models.CharField(max_length=300, help_text="Comma-separated technologies")
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    live_url = models.URLField(blank=True, help_text="Live project URL")
    github_url = models.URLField(blank=True, help_text="GitHub repository URL")
    featured = models.BooleanField(default=False)
    completion_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completion_date', '-created_at']

    def __str__(self):
        return self.title


# Blog/News model
class BlogPost(models.Model):
    """Model for blog posts and news."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    excerpt = models.TextField(blank=True, help_text="Short preview text")
    content = models.TextField(help_text="Full post content with HTML")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, blank=True,
                               choices=[
                                   ('news', 'Company News'),
                                   ('tech', 'Technology Updates'),
                                   ('case_study', 'Case Studies'),
                                   ('tutorial', 'Tutorials')
                               ])
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.title


class Item(models.Model):
	"""Legacy demo model - can be removed once other models are fully implemented."""

	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="items",
		null=True,
		blank=True,
	)

	def __str__(self):
		return self.name
