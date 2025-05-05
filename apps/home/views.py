from django.views.generic import TemplateView

from .models import MapsLocation


class HomeIndexView(TemplateView):
    template_name = "home/home_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "home_index_title": "Accueil",
                "results": "Les résultats ...",
            }
        )
        return context


class StationsMapFragmentView(TemplateView):
    template_name = "home/components/stations_map_fragment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "stations": list(
                    MapsLocation.objects.values(
                        "latitude", "longitude", "station_name", "address"
                    )
                ),
            }
        )
        return context
