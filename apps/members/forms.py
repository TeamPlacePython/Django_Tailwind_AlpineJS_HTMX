import datetime
from django import forms
from django.core.validators import RegexValidator

from apps.sport.models import SportsCategory
from .models import Member
from .constants import (
    GENDER_CHOICES,
    WEAPON_CHOICES,
    HANDENESS_CHOICES,
    ROLES_CHOICES,
)

ROLES_CHOICES_WITH_PLACEHOLDER = [
    ("", "Selectionnez un rôle...")
] + ROLES_CHOICES

GENDER_CHOICES_WITH_PLACEHOLDER = [
    ("", "Selectionnez un genre...")
] + GENDER_CHOICES

WEAPON_CHOICES_WITH_PLACEHOLDER = [
    ("", "Selectionnez une arme...")
] + WEAPON_CHOICES

HANDENESS_CHOICES_WITH_PLACEHOLDER = [
    ("", "Selectionnez la dominance manuelle...")
] + HANDENESS_CHOICES


class MemberForm(forms.ModelForm):
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "max": datetime.date.today().strftime("%Y-%m-%d"),
                "min": "1900-01-01",
            }
        ),
        input_formats=["%Y-%m-%d"],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure birth_date is properly initialized
        if self.instance and self.instance.birth_date:
            self.initial["birth_date"] = self.instance.birth_date.strftime(
                "%Y-%m-%d"
            )

    def clean_birth_date(self):
        return self.cleaned_data.get("birth_date")

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES_WITH_PLACEHOLDER,
        widget=forms.Select(
            attrs={
                "class": "form-control bg-navbar text-text_navbar_secondary"
            }
        ),
        required=False,
    )

    # Phone number validator
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{10,15}$",
        message=(
            "Phone number must be in format: '9999999999'. "
            "Maximum 15 digits allowed."
        ),
    )

    # Custom form fields
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex: 0612345678",
            }
        ),
    )

    postal_code = forms.CharField(
        max_length=5,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex: 06210",
            }
        ),
    )

    sports_category = forms.ModelChoiceField(
        queryset=SportsCategory.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control bg-navbar text-text_navbar_secondary"
            }
        ),
        required=False,
        empty_label="Selectionnez une catégorie...",
    )

    roles = forms.ChoiceField(
        choices=ROLES_CHOICES_WITH_PLACEHOLDER,
        widget=forms.Select(
            attrs={
                "class": "form-control bg-navbar text-text_navbar_secondary"
            }
        ),
        required=False,
    )

    weapon = forms.ChoiceField(
        choices=WEAPON_CHOICES_WITH_PLACEHOLDER,
        widget=forms.Select(
            attrs={
                "class": "form-control bg-navbar text-text_navbar_secondary"
            }
        ),
        required=False,
    )

    handeness = forms.ChoiceField(
        choices=HANDENESS_CHOICES_WITH_PLACEHOLDER,
        widget=forms.Select(
            attrs={
                "class": "form-control bg-navbar text-text_navbar_secondary"
            }
        ),
        required=False,
    )

    class Meta:
        model = Member
        fields = [
            "gender",
            "first_name",
            "last_name",
            "birth_date",
            "email",
            "phone_number",
            "address",
            "address_complement",
            "postal_code",
            "city",
            "sports_category",
            "weapon",
            "handeness",
            "roles",
            "status",
        ]
        widgets = {
            "gender": forms.Select(
                attrs={
                    "class": "form-control bg-navbar text-text_navbar_secondary"
                }
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last name"}
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "email@example.com",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Adresse",
                }
            ),
            "address_complement": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Complement d'adresse",
                }
            ),
            "postal_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ex: 06210"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "sports_category": forms.Select(
                attrs={
                    "class": "form-control bg-navbar text-text_navbar_secondary"
                }
            ),
            "weapon": forms.Select(
                attrs={
                    "class": "form-control bg-navbar text-text_navbar_secondary"
                }
            ),
            "handeness": forms.Select(
                attrs={"class": "form-control bg-navbar"}
            ),
            "roles": forms.Select(
                attrs={
                    "class": "form-control bg-navbar text-text_navbar_secondary"
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-control bg-navbar text-text_navbar_secondary"
                }
            ),
        }

    def clean_email(self):
        """Validate that the email is unique.

        Excludes the current instance when updating.
        """
        email = self.cleaned_data.get("email")
        if (
            email
            and Member.objects.filter(email=email)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        ):
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_postal_code(self):
        """Ensure that the postal code contains exactly 5 digits."""
        postal_code = self.cleaned_data.get("postal_code")
        if postal_code and (
            not postal_code.isdigit() or len(postal_code) != 5
        ):
            raise forms.ValidationError(
                "Postal code must contain exactly 5 digits."
            )
        return postal_code
