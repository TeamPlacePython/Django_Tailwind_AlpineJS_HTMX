from django.views.generic import TemplateView


class NavbarIndexView(TemplateView):
    template_name = "includes/header.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Accueil"
        context["user"] = self.request.user
        return context
