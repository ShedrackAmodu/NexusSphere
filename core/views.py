from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404

from .models import (
    Item, Contact, TeamMember, Service, PortfolioProject, BlogPost
)
from django.contrib.auth.forms import UserCreationForm


def signup(request):
	"""Simple signup view using Django's built-in UserCreationForm."""
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("login")
	else:
		form = UserCreationForm()
	return render(request, "registration/signup.html", {"form": form})


def index(request):
    """Render the project homepage for Phase 2."""
    from .models import Service, PortfolioProject

    services = Service.objects.all()[:6]  # Show up to 6 services
    featured_projects = PortfolioProject.objects.filter(featured=True)[:3]  # Show up to 3 featured projects

    return render(request, "index.html", {
        "project_name": "NexusSphere",
        "services": services,
        "featured_projects": featured_projects
    })


class ItemListView(ListView):
	model = Item
	template_name = "items/item_list.html"
	context_object_name = "items"


class ItemDetailView(DetailView):
	model = Item
	template_name = "items/item_detail.html"


class ItemCreateView(LoginRequiredMixin, CreateView):
	model = Item
	fields = ["name", "description"]
	template_name = "items/item_form.html"
	success_url = reverse_lazy("core:item_list")
	login_url = reverse_lazy("login")

	def form_valid(self, form):
		# assign owner to the logged-in user
		form.instance.owner = self.request.user
		return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Item
	fields = ["name", "description"]
	template_name = "items/item_form.html"
	success_url = reverse_lazy("core:item_list")
	login_url = reverse_lazy("login")
	raise_exception = True

	def test_func(self):
		obj = self.get_object()
		return (obj.owner is not None and obj.owner == self.request.user) or self.request.user.is_staff


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Item
	template_name = "items/item_confirm_delete.html"
	success_url = reverse_lazy("core:item_list")
	login_url = reverse_lazy("login")
	raise_exception = True

	def test_func(self):
		obj = self.get_object()
		return (obj.owner is not None and obj.owner == self.request.user) or self.request.user.is_staff


# Contact views
def contact_view(request):
    """Handle contact form submissions."""
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        company = request.POST.get('company', '')
        message = request.POST.get('message')

        if name and email and message:
            Contact.objects.create(
                name=name,
                email=email,
                company=company,
                message=message
            )
            messages.success(request, "Thank you for your message! We'll get back to you soon.")
            return redirect('core:contact')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, "contact.html")


# Team views
class TeamListView(ListView):
    model = TeamMember
    template_name = "team.html"
    context_object_name = "team_members"


# Services views
def services_view(request):
    """List all services, with optional filtering by expertise."""
    expertise_filter = request.GET.get('type')
    services = Service.objects.all()

    if expertise_filter:
        services = services.filter(expertise=expertise_filter)

    context = {
        'services': services,
        'expertise_filter': expertise_filter,
        'expertise_choices': dict(Service.EXPERTISE_CHOICES)
    }
    return render(request, "services.html", context)


# Portfolio views
class PortfolioListView(ListView):
    model = PortfolioProject
    template_name = "portfolio.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        expertise = self.request.GET.get('expertise')
        if expertise:
            queryset = queryset.filter(expertise=expertise)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expertise_choices'] = dict(PortfolioProject.EXPERTISE_CHOICES)
        context['current_expertise'] = self.request.GET.get('expertise')
        return context


def portfolio_detail_view(request, project_id):
    """Show portfolio project detail."""
    project = get_object_or_404(PortfolioProject, id=project_id)
    return render(request, "portfolio_detail.html", {"project": project})


# Blog views
class BlogListView(ListView):
    model = BlogPost
    template_name = "blog.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category, published=True)
        else:
            queryset = queryset.filter(published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = dict(BlogPost._meta.get_field('category').choices)
        context['current_category'] = self.request.GET.get('category')
        return context


def blog_detail_view(request, slug):
    """Show blog post detail."""
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return render(request, "blog_detail.html", {"post": post})


# Brochure download view
def brochure_view(request):
    """Return a PDF brochure for download."""
    # For now, create a simple placeholder PDF using reportlab if available
    # If reportlab is not installed, return a simple text response
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from django.http import HttpResponse
        from io import BytesIO

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Create content
        content = []
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=1  # center
        )

        content.append(Paragraph("NexusSphere Solutions - Company Brochure", title_style))
        content.append(Spacer(1, 12))

        content.append(Paragraph("Empowering Businesses with Innovative Technology Solutions", styles['Heading2']))

        # Add some content
        intro_text = """
        NexusSphere Solutions specializes in web applications, enterprise SaaS solutions,
        mobile applications, and cutting-edge technologies for geoscience platforms,
        school management systems, and CRM solutions.
        """
        content.append(Paragraph(intro_text, styles['Normal']))
        content.append(Spacer(1, 12))

        # Services section
        content.append(Paragraph("Our Services:", styles['Heading3']))
        services = [
            "• Web Applications",
            "• Enterprise SaaS Solutions",
            "• Mobile Applications",
            "• Geoscience Platforms",
            "• School Management Systems",
            "• CRM Solutions"
        ]
        for service in services:
            content.append(Paragraph(service, styles['Normal']))
            content.append(Spacer(1, 4))

        # Contact info
        content.append(Spacer(1, 12))
        content.append(Paragraph("Contact Us:", styles['Heading3']))
        content.append(Paragraph("Email: info@nexusspheresolutions.com", styles['Normal']))
        content.append(Paragraph("Phone: +1 (555) 123-4567", styles['Normal']))
        content.append(Paragraph("Website: https://nexusspheresolutions.com", styles['Normal']))

        doc.build(content)
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="nexussphere_brochure.pdf"'
        return response

    except ImportError:
        # If reportlab is not available, return a simple text response
        response = HttpResponse(
            "NexusSphere Solutions - Company Brochure\n\n"
            "Please contact us at info@nexusspheresolutions.com for our full brochure.\n\n"
            "Services:\n"
            "- Web Applications\n"
            "- Enterprise SaaS Solutions\n"
            "- Mobile Applications\n"
            "And more...",
            content_type='text/plain'
        )
        response['Content-Disposition'] = 'attachment; filename="nexussphere_brochure.txt"'
        return response


# Static page views
def about_view(request):
    """Render the about page."""
    return render(request, "about.html", {"project_name": "NexusSphere"})


def privacy_view(request):
    """Render the privacy policy page."""
    return render(request, "privacy.html", {"project_name": "NexusSphere"})


def terms_view(request):
    """Render the terms of service page."""
    return render(request, "terms.html", {"project_name": "NexusSphere"})
