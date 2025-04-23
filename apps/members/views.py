from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.utils.decorators import method_decorator

import random

from apps.sport.models import SportsCategory
from .models import Member
from .forms import MemberForm
from .mixins import MemberQuerysetMixin, HTMXMixin
from .constants import (
    HANDEDNESS_CHOICES,
    STATUS_CHOICES,
    ROLES_CHOICES,
    GENDER_CHOICES,
    WEAPON_CHOICES,
    STATUS_BADGES,
)
from apps.constant import (
    CONSTANT_CLOSE,
    CONSTANT_DELETE,
    CONSTANT_MODIFY,
    CONSTANT_SAVE,
    CONSTANT_UPDATE,
    CONSTANT_DETAILS,
)


class BaseMemberListView(MemberQuerysetMixin, ListView):
    model = Member
    context_object_name = "members"

    def get_filters(self):
        return {
            "search": self.request.GET.get("search"),
            "status": self.request.GET.get("status"),
            "category": self.request.GET.get("category"),
            "roles": self.request.GET.get("roles"),
            "gender": self.request.GET.get("gender"),
            "weapon": self.request.GET.get("weapon"),
            "handedness": self.request.GET.get("handedness"),
        }

    def apply_filters(self, queryset, filters):
        if filters["search"]:
            queryset = queryset.filter(
                Q(first_name__icontains=filters["search"])
                | Q(last_name__icontains=filters["search"])
                | Q(email__icontains=filters["search"])
            )

        filter_map = {
            "status": "status",
            "category": "sports_category_id",
            "roles": "roles",
            "gender": "gender",
            "weapon": "weapon",
            "handedness": "handedness",
        }

        for key, field in filter_map.items():
            if value := filters.get(key):
                queryset = queryset.filter(**{field: value})

        return queryset

    def get_queryset(self):
        filters = self.get_filters()
        queryset = super().get_queryset().order_by("first_name", "last_name")
        return self.apply_filters(queryset, filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Éléments de contexte génériques centralisés ici
        context.update(
            {
                "search_placeholder": "Recherche par nom...🔍",
                "button_reset_label": "Réinitialiser",
                "status_label": "Tous les statuts",
                "status_choices": STATUS_CHOICES,
                "category_label": "Toutes les catégories",
                "category_choices": SportsCategory.objects.all(),
                "role_label": "Tous les rôles",
                "roles_choices": ROLES_CHOICES,
                "gender_label": "Tous les genres",
                "gender_choices": GENDER_CHOICES,
                "weapon_label": "Toutes les armes",
                "weapon_choices": WEAPON_CHOICES,
                "handedness_label": "Toutes les mains",
                "handedness_choices": HANDEDNESS_CHOICES,
                "member_not_found_message": "Aucun membre trouvé",
                "status_badge_colors": STATUS_BADGES,
            }
        )
        return context


class MemberListView(BaseMemberListView):
    template_name = "members/member_list.html"
    paginate_by = 9
    _context_defaults = {
        "member_list_title": "Liste des membres ...",
        "member_list_description": "Liste des membres du club avec option de filtrage.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["button_details_label"] = CONSTANT_DETAILS
        context.update(self._context_defaults)
        return context


class MemberTableView(LoginRequiredMixin, BaseMemberListView):
    template_name = "members/members_table.html"
    _context_defaults = {
        "member_table_title": "Table des Membres ...",
        "member_table_description": "Table des membres de l'association.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
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
            }
        )
        context.update(self._context_defaults)
        return context


class MemberHomeView(TemplateView):
    template_name = "members/components/random_members_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["random_members"] = Member.objects.order_by("?")[:3]
        return context


class MemberEditView(
    LoginRequiredMixin, HTMXMixin, MemberQuerysetMixin, DetailView
):
    model = Member
    template_name = "members/modals/member_edit_modal.html"
    context_object_name = "member"

    def get_queryset(self):
        return super().get_queryset().select_related("sports_category")

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
                "member_personal_information_label": "Informations personnelles",
                "member_sports_information_label": "Informations sportives",
                "button_close_label": CONSTANT_CLOSE,
                "button_delete_label": CONSTANT_DELETE,
                "button_modify_label": CONSTANT_MODIFY,
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
    success_url = reverse_lazy("members:member_list")
    _context_defaults = {
        "member_create_update_title": "Créer un membre ...",
        "member_create_update_description": "Création d'un membre de l'association.",
    }

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.headers.get("HX-Request"):
            return HttpResponse(
                headers={
                    "HX-Redirect": self.success_url,
                }
            )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "button_avatar_label": "Ajouter un avatar",
                "button_close_label": CONSTANT_CLOSE,
                "button_save_label": CONSTANT_SAVE,
                **self._context_defaults,
            }
        )
        return context


class MemberUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = "members/member_form.html"
    success_url = reverse_lazy("members:member_list")
    success_message = "The member has been successfully updated."
    _context_defaults = {
        "member_create_update_description": "Modification d'un membre de l'association.",
    }

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return [self.template_name]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member_name = self.object.get_full_name()
        context["member_create_update_title"] = (
            f"Modification de {member_name}"
        )
        context.update(
            {
                "button_avatar_label": "Changer l'avatar",
                "button_save_label": CONSTANT_UPDATE,
                "button_close_label": CONSTANT_CLOSE,
                **self._context_defaults,
            }
        )
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.headers.get("HX-Request"):
            return HttpResponse(
                headers={
                    "HX-Redirect": self.success_url,
                }
            )
        return response


class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    template_name = "members/member_confirm_delete.html"
    success_url = reverse_lazy("members:member_list")

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
        context.update(
            {
                "member_confirmation_delete": f"Supprimer {member_name}",
                "member_avatar": self.object.photo,
                "button_close_label": CONSTANT_CLOSE,
                "button_confirmation_label": CONSTANT_DELETE,
            }
        )
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


@method_decorator(staff_member_required, name="dispatch")
class ResetMemberStatusView(View):
    def post(self, request, *args, **kwargs):
        today = now().date()
        try:
            updated_count = (
                Member.objects.filter(roles="member")
                .exclude(status="pending")
                .update(status="pending")
            )
        except Exception as e:
            return HttpResponse(f"Erreur : {str(e)}", status=500)

        html = render_to_string(
            "members/partials/reset_success_toast.html",
            {"updated_count": updated_count},
        )
        return HttpResponse(html)
