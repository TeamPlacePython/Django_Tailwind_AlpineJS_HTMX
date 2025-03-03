from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Member, SportsCategory
from .forms import MemberForm


class BaseMemberListView(LoginRequiredMixin, ListView):
    """
    Basic view for listing members, used by specific views (list and table).
    """

    model = Member
    context_object_name = "members"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("sports_category")
            .prefetch_related("roles", "tags")
            .order_by("first_name", "last_name")
        )

        search_query = self.request.GET.get("search")
        status_filter = self.request.GET.get("status")
        category_filter = self.request.GET.get("category")

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(email__icontains=search_query)
            )

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if category_filter:
            queryset = queryset.filter(sports_category_id=category_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "categories": SportsCategory.objects.all(),
                "status_choices": Member.STATUS_CHOICES,
                "modify": "Modifier",
                "not_found": "Aucun membre trouvé",
                "status_colors": {
                    "active": "actif",
                    "inactive": "inactif",
                    "pending": "attente",
                },
            }
        )
        return context


class MemberListView(BaseMemberListView):
    """Vue pour afficher les membres sous forme de cartes."""

    template_name = "members/member_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Membres",
                "team": "Club team ...",
                "search": "Rechercher un membre...",
                "all_status": "Tous les statuts",
                "all_categories": "Toutes les catégories",
                "show_details": "Voir détails",
                "description": (
                    "Liste des membres de l'organisation avec options de filtrage et de recherche."
                ),
            }
        )
        return context


class MemberTableView(BaseMemberListView):
    """View to display members as a table."""

    template_name = "members/members_table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Table des Membres ...",
                "description": ("Table des membres de l'association."),
            }
        )
        return context


class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = "members/member_detail.html"
    context_object_name = "member"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("sports_category")
            .prefetch_related("roles", "tags")
        )

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["members/member_detail.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.get_object()
        context.update(
            {
                "roles": member.roles.all(),
                "tags": member.tags.all(),
                # Adding data for status badges
                "status_colors": {
                    "active": "actif",
                    "inactive": "inactif",
                    "pending": "attente",
                },
                # Formatting dates if necessary
                "date_joined_formatted": member.date_joined.strftime(
                    "%d/%m/%Y"
                ),
                "last_updated_formatted": member.last_updated.strftime(
                    "%d/%m/%Y %H:%M"
                ),
            }
        )
        if self.request.headers.get("HX-Request"):
            context["is_modal"] = True
        return context


class MemberCreateView(LoginRequiredMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = "members/member_form.html"
    success_url = reverse_lazy("members:member-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Ajouter un membre ...",
                "button_text": "Ajouter",
            }
        )
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if photo := self.request.FILES.get("form_photo"):
            self.object.photo = photo
        self.object.save()
        form.save_m2m()

        messages.success(
            self.request,
            f"Le membre {self.object.get_full_name()} a été créé avec succès.",
        )

        if self.request.headers.get("HX-Request"):
            return HttpResponse(status=204)

        return HttpResponseRedirect(self.get_success_url())


class MemberUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    template_name = "members/member_form.html"
    form_class = MemberForm
    success_url = reverse_lazy("members:member-list")
    success_message = "Le membre a été mis à jour avec succès."

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["members/member_update_form_modal.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Modifier un membre ...",
                "button_text": "Mettre à jour",
            }
        )
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if "photo" in self.request.FILES:
            self.object.photo = self.request.FILES["photo"]
        self.object.save()
        if self.request.headers.get("HX-Request"):
            return HttpResponseRedirect(reverse_lazy("members:member-list"))
        return super().form_valid(form)


class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    template_name = "members/member_confirm_delete.html"
    success_url = reverse_lazy("members:member-list")

    def delete(self, request, *args, **kwargs):
        member = self.get_object()
        messages.success(
            self.request,
            f"Le membre {member.get_full_name()} a été supprimé avec succès.",
        )
        return super().delete(request, *args, **kwargs)


@require_POST
def update_photo(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if photo := request.FILES.get("photo"):
        member.photo = photo
        member.save()
        # Renvoyer le HTML de la nouvelle image
        return HttpResponse(
            f'<img id="member-photo" src="{member.photo.url}" alt="Photo du membre" class="w-36 h-36 rounded-full object-cover my-4 border-2 border-text_navbar">'
        )
    return JsonResponse({"error": "Aucune photo téléchargée."}, status=400)
