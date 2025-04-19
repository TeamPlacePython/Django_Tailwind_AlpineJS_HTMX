from django.views.generic import ListView
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.http import HttpResponse

from .models import SportsCategory, Event, Result
from .utils.grouping import group_results_by_event_and_category


CONST_RESPECT_INSTRUCTIONS = "Tous les tireurs du club s'engagent à respecter les consignes données par le maître d'armes."


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
        context.update(
            {
                "sport_category_name": "Catégories",
                "sport_category_description": "Description",
                "sport_category_born_start": "Naissance de",
                "sport_category_born_end": "Jusqu'à",
                "sport_category_price": "Montant",
                "respect_instructions": CONST_RESPECT_INSTRUCTIONS,
                **self._context_defaults,
            }
        )
        return context


class TrainingHoursView(TemplateView):
    template_name = "sport/sport_training_hours_table.html"
    _context_defaults = {
        "sport_category_price_title": "Horaires des entraînements ...",
        "sport_category_price_description": "Liste des horaires des entraînements selon les catégories.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Load only the necessary fields
        categories = SportsCategory.objects.values(
            "name",
            "monday_hours",
            "tuesday_hours",
            "wednesday_hours",
            "thursday_hours",
            "friday_hours",
        )

        # Build the timetable dictionary
        schedule = {
            category["name"]: {
                "Lundi": category["monday_hours"],
                "Mardi": category["tuesday_hours"],
                "Mercredi": category["wednesday_hours"],
                "Jeudi": category["thursday_hours"],
                "Vendredi": category["friday_hours"],
            }
            for category in categories
        }

        # Context update in one go
        context.update(
            {
                "schedule": schedule,
                "sport_category": "Catégorie",
                "monday": "Lundi",
                "tuesday": "Mardi",
                "wednesday": "Mercredi",
                "thursday": "Jeudi",
                "friday": "Vendredi",
                "respect_instructions": CONST_RESPECT_INSTRUCTIONS,
                **self._context_defaults,
            }
        )
        return context


class ResultsListView(ListView):
    model = Result
    template_name = "sport/results_list.html"
    context_object_name = "results"

    def get_queryset(self):
        queryset = Result.objects.select_related("member", "event").order_by(
            "-event__date"
        )
        if event_id := self.request.GET.get("event"):
            queryset = queryset.filter(event_id=event_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = self.get_events()
        context["grouped_results"] = self.get_grouped_results()
        context["selected_event_id"] = self.request.GET.get("event")
        return context

    def get_events(self):
        return Event.objects.order_by("-date")

    def get_grouped_results(self):
        results = self.get_queryset()
        return group_results_by_event_and_category(results)

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("HX-Request"):
            html = render_to_string(
                "sport/results_table_fragment.html", context
            )
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)
