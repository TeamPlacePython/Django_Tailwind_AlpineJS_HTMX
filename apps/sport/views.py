from django.views.generic import ListView
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.timezone import now
from datetime import timedelta

from .models import SportsCategory, Event, Result
from .utils.grouping import group_results_by_event_and_category

CONST_RESPECT_INSTRUCTIONS = "Tous les tireurs du club s'engagent à respecter les consignes données par le maître d'armes."


class SportsContextMixin:
    respect_instructions = CONST_RESPECT_INSTRUCTIONS

    def get_common_labels(self):
        return {
            "respect_instructions": self.respect_instructions,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_labels())
        return context


class SportsCategoryListView(SportsContextMixin, ListView):
    model = SportsCategory
    context_object_name = "sport_category"
    template_name = "sport/sport_category_prices_table.html"

    _context_defaults = {
        "sport_category_price_title": "Cotisations 2024 / 2025 ...",
        "sport_category_price_description": "Liste des catégories de sports avec les montants des cotisations.",
        "sport_category_name": "Catégories",
        "sport_category_description": "Description",
        "sport_category_born_start": "Naissance de",
        "sport_category_born_end": "Jusqu'à",
        "sport_category_price": "Montant",
    }

    def get_queryset(self):
        return super().get_queryset().order_by("-start_year")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._context_defaults)
        return context


class TrainingHoursView(SportsContextMixin, TemplateView):
    template_name = "sport/sport_training_hours_table.html"

    _context_defaults = {
        "sport_category_price_title": "Horaires des entraînements ...",
        "sport_category_price_description": "Liste des horaires des entraînements selon les catégories.",
        "sport_category": "Catégorie",
        "monday": "Lundi",
        "tuesday": "Mardi",
        "wednesday": "Mercredi",
        "thursday": "Jeudi",
        "friday": "Vendredi",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = SportsCategory.objects.values(
            "name",
            "monday_hours",
            "tuesday_hours",
            "wednesday_hours",
            "thursday_hours",
            "friday_hours",
        )

        context["schedule"] = {
            cat["name"]: {
                "Lundi": cat["monday_hours"],
                "Mardi": cat["tuesday_hours"],
                "Mercredi": cat["wednesday_hours"],
                "Jeudi": cat["thursday_hours"],
                "Vendredi": cat["friday_hours"],
            }
            for cat in categories
        }

        context.update(self._context_defaults)
        return context


class GroupedResultsMixin:
    def get_grouped_results(self, limit=None, event_id=None):
        queryset = Result.objects.select_related(
            "member__sports_category", "event"
        ).order_by("-event__date", "member__sports_category__name")

        if event_id:
            queryset = queryset.filter(event_id=event_id)

        if limit:
            queryset = queryset[:limit]

        return group_results_by_event_and_category(queryset)


class ResultsListView(GroupedResultsMixin, ListView):
    model = Result
    template_name = "sport/results_list.html"
    context_object_name = "results"

    def get_queryset(self):
        qs = Result.objects.select_related("member", "event").order_by(
            "-event__date"
        )
        if event_id := self.request.GET.get("event"):
            qs = qs.filter(event_id=event_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_event_id = self.request.GET.get("event")
        context.update(
            {
                "events": Event.objects.order_by("-date"),
                "grouped_results": self.get_grouped_results(
                    event_id=selected_event_id
                ),
                "selected_event_id": selected_event_id,
            }
        )
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("HX-Request"):
            html = render_to_string(
                "sport/results_table_fragment.html", context
            )
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class ResultEventHomeView(GroupedResultsMixin, TemplateView):
    template_name = "sport/components/result_event_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["grouped_results"] = self.get_grouped_results(limit=2)
        return context


class UpcomingEventHomeView(GroupedResultsMixin, TemplateView):
    template_name = "sport/components/upcoming_event_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "upcoming_events": self.get_upcoming_events(),
                "grouped_results": self.get_grouped_results(limit=2),
            }
        )
        return context

    def get_upcoming_events(self):
        return Event.objects.filter(
            date__gte=now() - timedelta(hours=24)
        ).order_by("date")
