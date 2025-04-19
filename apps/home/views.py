from django.utils.timezone import now
from django.views.generic import TemplateView
from datetime import timedelta
import random

from apps.sport.utils.grouping import group_results_by_event_and_category
from apps.sport.models import Event, Result
from apps.posts.models import Post
from apps.members.models import Member
from .models import MapsLocation, CarouselImage


class HomeIndexView(TemplateView):
    template_name = "home/home_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "stations": self.get_stations(),
                "carousel_images": self.get_carousel_images(),
                "posts": self.get_posts(),
                "upcoming_events": self.get_upcoming_events(),
                "grouped_results": self.get_grouped_results(),
                "random_members": self.get_random_members(),
                "home_index_title": "Accueil",
                "carousel_home_index_title": "Entre tradition et modernité ...",
                "results": "Les résultats ...",
            }
        )
        return context

    def get_stations(self):
        return list(
            MapsLocation.objects.values(
                "latitude",
                "longitude",
                "station_name",
                "address",
            )
        )

    def get_carousel_images(self):
        return CarouselImage.objects.all()[:10]

    def get_posts(self):
        return Post.objects.all()[:3]

    def get_upcoming_events(self):
        return Event.objects.filter(
            date__gte=now() - timedelta(hours=24)
        ).order_by("date")

    def get_grouped_results(self):
        results = Result.objects.select_related(
            "member__sports_category", "event"
        ).order_by("-event__date", "member__sports_category__name")[:2]
        return group_results_by_event_and_category(results)

    def get_random_members(self, count=3):
        member_ids = list(Member.objects.values_list("id", flat=True))
        if len(member_ids) <= count:
            return Member.objects.filter(id__in=member_ids)

        random_ids = random.sample(member_ids, count)
        # Optionnel : garder l'ordre aléatoire d'origine
        preserved_order = {id_: i for i, id_ in enumerate(random_ids)}
        members = list(Member.objects.filter(id__in=random_ids))
        return sorted(members, key=lambda m: preserved_order[m.id])
