from django.utils.timezone import now
from django.views.generic import TemplateView
from django.views.generic import ListView
from itertools import groupby
from datetime import timedelta
import re
from apps.sport.models import SportsCategory
from .models import MapsLocation, CarouselImage, Event, Result

CONST_RESPECT_INSTRUCTONS = "Tous les tireurs du club s'engagent à respecter les consignes données par le maître d'armes."


class HomeIndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ajouter les stations au contexte
        context["stations"] = list(
            MapsLocation.objects.values(
                "latitude",
                "longitude",
                "station_name",
                "address",
            )
        )

        # Ajouter les 10 dernières images du carrousel
        context["carousel_images"] = CarouselImage.objects.all()[:10]

        # Ajouter les événements à venir (triés par date)
        context["upcoming_events"] = Event.objects.filter(
            date__gte=now() - timedelta(hours=24)
        ).order_by("date")

        context["home_index_title"] = "Accueil"
        context["carousel_home_index_title"] = (
            "Entre tradition et modernité ..."
        )
        context["results"] = "Les résultats ..."

        # Ajouter les résultats des événements passés
        results = Result.objects.select_related(
            "member__sports_category", "event"
        ).order_by(
            "event__date", "event__title", "member__sports_category__name"
        )

        # Fonction pour extraire le numéro après "M-"
        def extract_number(category):
            match = re.search(r"M-(\d+)", category.name if category else "")
            return int(match[1]) if match else float("inf")

        # Grouper par événement et catégorie sportive
        grouped_results = []
        for (event, category), group in groupby(
            results, key=lambda r: (r.event, r.member.sports_category)
        ):
            grouped_results.append(
                {
                    "event_title": event.title,
                    "event_date": event.date,
                    "sports_category": category.name,
                    # Clé de tri basée sur le numéro
                    "sort_key": extract_number(category),
                    # Liste des résultats pour cet événement et cette catégorie
                    "members": list(group),
                }
            )

        # Trier par la clé "sort_key" (numéro après "M-")
        grouped_results.sort(key=lambda x: x["sort_key"])
        context["grouped_results"] = grouped_results

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
                "respect_instructions": CONST_RESPECT_INSTRUCTONS,
                **self._context_defaults,
            }
        )
        return context


class SportHistoryView(TemplateView):
    template_name = "sport/sport_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message_board_title"] = "L'Histoire de l'Escrime"
        context["message_board_description"] = (
            "Découvrez les origines et l'évolution de l'escrime à travers les âges."
        )
        return context


class ResultsListView(ListView):
    model = Result
    template_name = "home/results_list.html"
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

        # Ajouter les événements à filtrer
        context["events"] = Event.objects.order_by("-date")

        # Grouper les résultats par événement et catégorie sportive
        results = self.get_queryset()

        # Fonction pour extraire le numéro après "M-"
        def extract_number(category):
            match = re.search(r"M-(\d+)", category.name if category else "")
            return int(match[1]) if match else float("inf")

        grouped_results = []
        for (event, category), group in groupby(
            results, key=lambda r: (r.event, r.member.sports_category)
        ):
            grouped_results.append(
                {
                    "event_title": event.title,
                    "event_date": event.date,
                    "sports_category": category.name,
                    "sort_key": extract_number(category),
                    "members": list(group),
                }
            )

        # Trier par la clé "sort_key" (numéro après "M-")
        grouped_results.sort(key=lambda x: x["sort_key"])

        context["grouped_results"] = grouped_results

        return context
