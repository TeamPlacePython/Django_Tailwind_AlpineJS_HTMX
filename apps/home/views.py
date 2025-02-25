from django.views.generic import TemplateView


class HomeIndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Accueil"
        context["hero_title"] = "Salle d'escrime de Mandelieu"
        context["hero_slogan"] = "Maîtrisez la lame, forgez votre légende"
        context["connect"] = "Se connecter"
        return context
