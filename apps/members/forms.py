from django import forms
from django.core.validators import RegexValidator
import datetime
from .models import Member


class MemberForm(forms.ModelForm):
    # Validateur pour le numéro de téléphone
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{10,15}$",
        message=(
            "Le numéro de téléphone doit être au format : '9999999999'. "
            "Maximum 15 chiffres autorisés."
        ),
    )

    # Personnalisation des champs
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

    class Meta:
        model = Member
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "email",
            "phone_number",
            "address",
            "postal_code",
            "city",
            "sports_category",
            "status",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Prénom",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nom de famille",
                }
            ),
            "birth_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Date de naissance",
                    "type": "date",
                    "max": datetime.date.today().strftime("%Y-%m-%d"),
                    "min": "1900-01-01",
                },
                format="%d/%m/%Y",
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "email@exemple.com",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Rue",
                }
            ),
            "postal_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: 06210",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ville",
                }
            ),
            "sports_category": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control mb-7"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            email
            and Member.objects.filter(email=email)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        ):
            # Checks if the email already exists, excluding the current instance in case of update
            raise forms.ValidationError(
                "Cette adresse email est déjà utilisée."
            )
        return email

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get("postal_code")
        if postal_code and (
            not postal_code.isdigit() or len(postal_code) != 5
        ):
            # Verify that the postal code contains exactly 5 digits
            raise forms.ValidationError(
                "Le code postal doit contenir exactement 5 chiffres."
            )
        return postal_code
