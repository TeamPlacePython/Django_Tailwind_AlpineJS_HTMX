from django.contrib.auth.mixins import LoginRequiredMixin
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
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Member, SportsCategory
from .forms import MemberForm


# Vues pour Member
class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    template_name = "members/member_list.html"
    context_object_name = "members"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("sports_category")  # Précharge la catégorie
            .prefetch_related(
                "roles", "tags"
            )  # Précharge les relations many-to-many
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
        context["categories"] = SportsCategory.objects.all()
        context["status_choices"] = Member.STATUS_CHOICES
        context["title"] = "Membres"
        context["description"] = (
            "Liste des membres de l'organisation avec options de filtrage et de recherche."
        )
        context["search"] = "Rechercher un membre..."
        context["filter"] = "Filtrer par statut"
        context["selected"] = "Selected"
        context["all_status"] = "Tous les statuts"
        context["all_categories"] = "Toutes les catégories"
        context["show_details"] = "Voir détails"
        context["modify"] = "Modifier"
        context["not_found"] = "Aucun membre trouvé"
        # Ajout des couleurs pour les badges de statut
        context["status_colors"] = {
            "active": "actif",
            "inactive": "inactif",
            "pending": "attente",
        }
        return context


class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = "members/member_detail_modal.html"
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
            return ["members/member_detail_modal.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.get_object()
        context["roles"] = member.roles.all()
        context["tags"] = member.tags.all()
        # Ajout des données pour les badges de statut
        context["status_colors"] = {
            "active": "actif",
            "inactive": "inactif",
            "pending": "attente",
        }
        # Formatage des dates si nécessaire
        context["date_joined_formatted"] = member.date_joined.strftime(
            "%d/%m/%Y"
        )
        context["last_updated_formatted"] = member.last_updated.strftime(
            "%d/%m/%Y %H:%M"
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
        context["title"] = "Ajouter un membre"
        context["button_text"] = "Ajouter"
        return context

    def form_valid(self, form):
        # Sauvegarder le formulaire sans commit pour pouvoir modifier l'instance
        self.object = form.save(commit=False)

        # Récupérer le fichier photo depuis le champ caché
        photo_file = self.request.FILES.get("form_photo")
        if photo_file:
            self.object.photo = photo_file

        # Sauvegarder définitivement
        self.object.save()

        # Sauvegarder les relations many-to-many
        form.save_m2m()

        messages.success(
            self.request,
            f"Le membre {self.object.get_full_name()} a été créé avec succès.",
        )

        if self.request.headers.get("HX-Request"):
            return HttpResponse(status=204)

        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    template_name = "members/member_form.html"
    form_class = MemberForm
    success_url = reverse_lazy("members:member-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, "Le membre a été mis à jour avec succès."
        )
        if self.request.headers.get("HX-Request"):
            # Si c'est une requête HTMX, rediriger vers la liste des membres
            return HttpResponseRedirect(reverse_lazy("members:member-list"))
        return response

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["members/member_form_modal.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modifier un membre"
        context["button_text"] = "Mettre à jour"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "photo" in request.FILES:
            self.object.photo = request.FILES["photo"]
            self.object.save()
            return HttpResponse(status=204)

        return super().post(request, *args, **kwargs)


class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    template_name = "members/member_confirm_delete.html"
    success_url = reverse_lazy("member-list")

    def delete(self, request, *args, **kwargs):
        member = self.get_object()
        messages.success(
            self.request,
            f"Le membre {member.get_full_name()} a été supprimé avec succès.",
        )
        return super().delete(request, *args, **kwargs)


@require_POST
def update_member_photo(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if "photo" in request.FILES:
        member.photo = request.FILES["photo"]
        member.save()

        # Retourne uniquement l'image mise à jour
        html = f"""
            <img id="member-photo" 
                 src="{member.photo.url}" 
                 alt="Photo du membre"
                 class="w-36 h-36 rounded-full object-cover my-4 
                        border-2 border-text_navbar">
        """
        return HttpResponse(html)
    return HttpResponse(status=400)
