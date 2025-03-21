from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Member, SportsCategory
from .forms import MemberForm
from .mixins import MemberQuerysetMixin, HTMXMixin
from .constants import (
    HANDENESS_CHOICES,
    STATUS_CHOICES,
    ROLES_CHOICES,
    GENDER_CHOICES,
    WEAPON_CHOICES,
    STATUS_BADGES,
)
import random

CONSTANT_CLOSE = "Fermer"


class BaseMemberListView(LoginRequiredMixin, MemberQuerysetMixin, ListView):
    model = Member
    context_object_name = "members"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by("first_name", "last_name")
        search_query = self.request.GET.get("search")
        status_filter = self.request.GET.get("status")
        category_filter = self.request.GET.get("category")
        roles_filter = self.request.GET.get("roles")
        gender_filter = self.request.GET.get("gender")
        weapon_filter = self.request.GET.get("weapon")
        handeness_filter = self.request.GET.get("handeness")

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

        if roles_filter:
            queryset = queryset.filter(roles=roles_filter)

        if gender_filter:
            queryset = queryset.filter(gender=gender_filter)

        if weapon_filter:
            queryset = queryset.filter(weapon=weapon_filter)

        if handeness_filter:
            queryset = queryset.filter(handeness=handeness_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "search_placeholder": "Recherche par nom...",
                "button_reset_label": "Réinitialiser",
                "status_all_label": "Tous les statuts",
                "status_choices": STATUS_CHOICES,
                "category_all_label": "Toutes les catégories",
                "category_choices": SportsCategory.objects.all(),
                "role_all_label": "Tous les rôles",
                "roles_choices": ROLES_CHOICES,
                "gender_all_label": "Tous les genres",
                "gender_choices": GENDER_CHOICES,
                "weapon_all_label": "Toutes les armes",
                "weapon_choices": WEAPON_CHOICES,
                "handedness_all_label": "Toutes les mains",
                "handeness_choices": HANDENESS_CHOICES,
                "member_not_found_message": "Aucun membre trouvé",
                "status_badge_colors": STATUS_BADGES,
            }
        )

        return context


class MemberListView(BaseMemberListView):
    template_name = "members/member_list.html"
    _context_defaults = {
        "message_section_title": "Liste des membres ...",
        "message_section_description": "Liste des membres du club avec option de filtrage.",
        "button_details_label": "Voir détails",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._context_defaults)
        return context


class MemberTableView(BaseMemberListView):
    template_name = "members/members_table.html"
    _context_defaults = {
        "member_table_title": "Table des Membres ...",
        "member_table_description": "Table des membres de l'association.",
        "member_avatars_label": "Avatars",
        "member_first_name_label": "Prénom",
        "member_last_name_label": "Nom",
        "member_gender_label": "Genre",
        "member_email_label": "Email",
        "member_phone_label": "Téléphone",
        "member_birth_date_label": "Date de naissance",
        "member_category_label": "Catégories",
        "member_status_label": "Status",
        "member_role_label": "Rôles",
        "member_weapon_label": "Arme",
        "member_handedness_label": "Main",
        "member_not_found_message": "Aucun membre trouvé.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._context_defaults)
        return context


class MemberDetailView(
    LoginRequiredMixin, HTMXMixin, MemberQuerysetMixin, DetailView
):
    model = Member
    template_name = "members/member_detail_modal.html"
    context_object_name = "member"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("sports_category")
            .prefetch_related("tags")
        )

    def get_template_names(self):
        return self.get_htmx_template(self.template_name, self.template_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.object
        context.update(
            {
                "date_joined_formatted": member.date_joined.strftime(
                    "%d/%m/%Y"
                ),
                "last_updated_formatted": member.last_updated.strftime(
                    "%d/%m/%Y %H:%M"
                ),
                "button_close_label": CONSTANT_CLOSE,
                "member_personal_information_label": "Informations personnelles",
                "member_sports_information_label": "Informations sportives",
                "button_modify_label": "Modifier",
            }
        )
        if self.is_htmx_request():
            context["is_modal"] = True
        return context

    def get_latest_membership_fee(self):
        latest_fee = self.fees.filter(is_valid=True).first()
        return latest_fee.amount if latest_fee else None


class MemberCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = "members/member_form.html"
    _htmx_template = ["members/member_form.html"]
    _regular_template = ["members/member_form.html"]
    success_url = reverse_lazy("members:member-list")
    success_message = "The member has been successfully created."
    _context_defaults = {
        "member_title": "Créer un membre ...",
        "member_avatar_label": "Ajouter un avatar",
        "button_close_label": CONSTANT_CLOSE,
        "button_save_label": "Enregistrer",
    }

    def get_template_names(self):
        return (
            self._htmx_template
            if self.request.headers.get("HX-Request")
            else self._regular_template
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._context_defaults)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.headers.get("HX-Request"):
            response = HttpResponse()
            response["HX-Redirect"] = self.success_url

        return response


class MemberUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = "members/member_form.html"
    success_url = reverse_lazy("members:member-list")
    success_message = "The member has been successfully updated."
    _context_defaults = {
        "member_avatar_label": "Changer l'avatar",
        "button_save_label": "Mise à jour",
        "button_close_label": CONSTANT_CLOSE,
    }

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return [self.template_name]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member_name = self.object.get_full_name()
        context["member_title"] = f"Modification de {member_name}"
        context.update(self._context_defaults)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.headers.get("HX-Request"):
            response = HttpResponse()
            response["HX-Redirect"] = self.success_url
        return response


class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    template_name = "members/member_confirm_delete.html"
    success_url = reverse_lazy("members:member-list")

    def delete(self, request, *args, **kwargs):
        member = self.get_object()
        messages.success(
            self.request,
            f"The member {member.get_full_name()} has been successfully deleted.",
        )
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member_name = self.object.get_full_name()
        context["member_title"] = f"Suppression de {member_name}"
        return context


class UpdatePhotoView(View):
    def post(self, request, pk):
        member = get_object_or_404(Member, pk=pk)

        # Checks if a photo is present in the files
        if "photo" not in request.FILES:
            return JsonResponse({"error": "Aucune photo envoyée."}, status=400)

        # Updates the photo
        member.photo = request.FILES["photo"]
        member.save()

        # Adds a "cache buster" to avoid browser caching
        cache_buster = random.randint(1000, 9999)
        photo_url = f"{member.photo.url}?v={cache_buster}"

        return JsonResponse({"photo_url": photo_url})
