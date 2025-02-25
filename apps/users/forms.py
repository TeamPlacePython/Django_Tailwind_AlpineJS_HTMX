from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Profile


class ProfileForm(ModelForm):
    """
    Form for updating user profile information.
    Handles profile image, display name and additional information.

    Validates that display name is at least 2 characters long.
    """

    class Meta:
        model = Profile
        fields = ["image", "displayname", "info"]
        widgets = {
            "image": forms.FileInput(attrs={"accept": "image/*"}),
            "displayname": forms.TextInput(
                attrs={
                    "placeholder": _("Add display name"),
                    "minlength": "2",
                    "maxlength": "20",
                }
            ),
            "info": forms.Textarea(
                attrs={"rows": 3, "placeholder": _("Add information")}
            ),
        }

    def clean_displayname(self):
        displayname = self.cleaned_data.get("displayname")
        if displayname and len(displayname.strip()) < 2:
            raise forms.ValidationError(
                _("The display name must contain at least 2 characters.")
            )
        return displayname.strip() if displayname else displayname


class EmailForm(ModelForm):
    """
    Form for updating user's email address.
    Requires a valid email address input.
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": _("Email address")}),
    )

    class Meta:
        model = User
        fields = ["email"]


class UsernameForm(ModelForm):
    """
    Form for updating username.
    Allows users to modify their username while maintaining Django's built-in validation.
    """

    class Meta:
        model = User
        fields = ["username"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": _("Username")})
        }
