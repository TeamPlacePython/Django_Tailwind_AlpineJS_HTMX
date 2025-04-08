from django.views.generic import TemplateView


class HistoryView(TemplateView):
    template_name = "history/history_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message_board_title"] = "L'Histoire de l'Escrime"
        context["message_board_description"] = (
            "Découvrez les origines et l'évolution de l'escrime à travers les âges."
        )
        return context
