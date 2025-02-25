from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.utils.translation import gettext_lazy as _
from allauth.account.utils import send_email_confirmation
from .forms import ProfileForm, EmailForm, UsernameForm


class ProfileView(View):
    """View to display a user profile.

    Allows displaying either the connected user's profile
    or another user's profile specified by their username.
    """

    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        """Generate context data with additional variables."""
        context = kwargs
        context["title"] = "Profil"
        return context

    def get(self, request, username=None):
        """Handle GET request to display a profile.

        Args:
            request: The HTTP request
            username: The username of the profile to display (optional)

        Returns:
            HTML page with profile information
        """
        if username:
            profile = get_object_or_404(
                User, username=username.lower()
            ).profile
        else:
            try:
                profile = request.user.profile
            except User.DoesNotExist:
                return redirect_to_login(request.get_full_path())

        context = self.get_context_data(profile=profile)
        return render(request, self.template_name, context=context)


class ProfileEditView(LoginRequiredMixin, View):
    """View to edit user profile information.

    Requires user authentication.
    """

    template_name = "users/profile_edit.html"
    form_class = ProfileForm

    def get_context_data(self, **kwargs):
        """Generate context data with additional variables."""
        context = kwargs
        context["title"] = "Edit"
        context["complete"] = "Complétez votre profil"
        context["modify"] = "Modification"
        context["submit"] = "Valider"
        context["skip"] = "Ignorer"
        context["cancel"] = "Annuler"
        return context

    def get(self, request):
        """Display the profile edit form."""
        form = self.form_class(instance=request.user.profile)
        onboarding = request.path == reverse("users:profile-onboarding")

        context = self.get_context_data(form=form, onboarding=onboarding)
        return render(request, self.template_name, context=context)

    def post(self, request):
        """Handle profile edit form submission."""
        form = self.form_class(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            return redirect("users:profile")

        onboarding = request.path == reverse("users:profile-onboarding")
        context = self.get_context_data(form=form, onboarding=onboarding)
        return render(request, self.template_name, context=context)


class ProfileSettingsView(LoginRequiredMixin, View):
    """View to display user profile settings.

    Requires user authentication.
    """

    template_name = "users/profile_settings.html"

    def get_context_data(self, **kwargs):
        """Generate context data with additional variables."""
        context = kwargs
        context["title"] = "Paramètres"
        context["email_address"] = "Adresse email"
        context["no_email"] = "Pas d'email"
        context["edit"] = "Editer"
        context["verified"] = "Vérifié"
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context=context)


class ProfileEmailChangeView(LoginRequiredMixin, View):
    """View to change user's email address.

    Requires user authentication.
    Sends confirmation email to new address.
    """

    template_name = "partials/email_form.html"
    form_class = EmailForm

    def get(self, request):
        """Display email change form.

        Args:
            request: The HTTP request

        Returns:
            Email change form if HTMX request,
            otherwise redirects to settings
        """
        if request.htmx:
            form = self.form_class(instance=request.user)
            context = {"form": form}
            return render(request, self.template_name, context=context)
        return redirect("users:profile-settings")

    def post(self, request):
        """Handle email change form submission.

        Args:
            request: The HTTP request

        Returns:
            Redirects to settings with success or error message
        """
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if (
                User.objects.filter(email=email)
                .exclude(id=request.user.id)
                .exists()
            ):
                messages.warning(request, f"{email} is already in use.")
                return redirect("users:profile-settings")

            form.save()
            send_email_confirmation(request, request.user)
            return redirect("users:profile-settings")

        messages.warning(request, "Email not valid or already in use")
        return redirect("users:profile-settings")


class ProfileUsernameChangeView(LoginRequiredMixin, View):
    """View to change username.

    Requires user authentication.
    """

    template_name = "partials/username_form.html"
    form_class = UsernameForm

    def get(self, request):
        """Display username change form.

        Args:
            request: The HTTP request

        Returns:
            Username form if HTMX request,
            otherwise redirects to settings
        """
        if request.htmx:
            form = self.form_class(instance=request.user)
            context = {"form": form}
            return render(request, self.template_name, context=context)
        return redirect("users:profile-settings")

    def post(self, request):
        """Handle username change form submission.

        Args:
            request: The HTTP request

        Returns:
            Redirects to settings with success or error message
        """
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            username = form.cleaned_data["username"].lower()
            if (
                User.objects.filter(username=username)
                .exclude(id=request.user.id)
                .exists()
            ):
                messages.warning(request, _("This username is already in use"))
                return redirect("users:profile-settings")
            form.save()
            messages.success(request, _("Username successfully updated"))
            return redirect("users:profile-settings")
        messages.warning(request, _("Invalid or already used username"))
        return redirect("users:profile-settings")


class ProfileEmailVerifyView(LoginRequiredMixin, View):
    """View to resend verification email.

    Requires user authentication.
    """

    def get(self, request):
        """Resend verification email.

        Args:
            request: The HTTP request

        Returns:
            Redirects to settings
        """
        send_email_confirmation(request, request.user)
        return redirect("users:profile-settings")


class ProfileDeleteView(LoginRequiredMixin, View):
    """View to delete user account.

    Requires user authentication.
    """

    template_name = "users/profile_delete.html"

    def get(self, request):
        """Display account deletion confirmation page.

        Args:
            request: The HTTP request

        Returns:
            The confirmation page
        """
        return render(request, self.template_name)

    def post(self, request):
        """Handle account deletion request.

        Args:
            request: The HTTP request

        Returns:
            Redirects to home page with confirmation message
        """
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Account deleted, what a pity")
        return redirect("home:home-index")
