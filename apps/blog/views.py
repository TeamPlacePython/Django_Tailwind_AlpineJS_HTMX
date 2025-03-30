from django.views.generic import TemplateView
from .models import Blog


class BlogIndexView(TemplateView):
    template_name = "blog/blog_index.html"  # Spécifie le template à rendre

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog_posts"] = self.get_blog_posts()
        return context

    def get_blog_posts(self):
        return Blog.objects.all()
