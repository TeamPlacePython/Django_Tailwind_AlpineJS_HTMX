from django.views.generic import TemplateView
from .models import MapsLocation


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
        return context
