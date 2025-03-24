from django.views.generic import ListView
from django.views.generic import TemplateView
from .models import SportsCategory


class SportsCategoryListView(ListView):
    model = SportsCategory
    context_object_name = "sport_category"
    template_name = "sport/sport_category_prices_table.html"
    _context_defaults = {
        "sport_category_price_title": "Cotisations 2024 / 2025 ...",
        "sport_category_price_description": "Liste des catégories de sports avec les montants des cotisations.",
    }

    def get_queryset(self):
        return super().get_queryset().order_by("-start_year")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._context_defaults)
        return context


class TrainingHoursView(TemplateView):
    template_name = "sport/sport_training_hours.html"
    _context_defaults = {
        "sport_category_price_title": "Horaires des d'entrainements ...",
        "sport_category_price_description": "Liste des horaires des entrainements selon les catégories.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Charger les informations des catégories et horaires
        categories = SportsCategory.objects.all()

        # Structure des horaires : {catégorie: {jour: "08:00 - 10:00"}}
        schedule = {}
        for category in categories:
            if category.name not in schedule:
                schedule[category.name] = {
                    "Lundi": category.monday_hours,
                    "Mardi": category.tuesday_hours,
                    "Mercredi": category.wednesday_hours,
                    "Jeudi": category.thursday_hours,
                    "Vendredi": category.friday_hours,
                }

        context["schedule"] = schedule
        context.update(self._context_defaults)
        return context
