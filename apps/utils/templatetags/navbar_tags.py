from django import template
from django.urls import reverse

register = template.Library()


@register.inclusion_tag("includes/header.html")
def render_navbar(user):
    """Rendu de la navbar selon l'état de l'utilisateur (authentifié ou non)"""
    print(f"User: {user}, Type: {type(user)}")
    if user.is_authenticated:
        return {
            "profile_items": [
                {"name": "My Profile", "url": reverse("users:profile")},
                {"name": "Edit Profile", "url": reverse("users:profile-edit")},
                {"name": "Settings", "url": reverse("users:profile-settings")},
                {"name": "Log Out", "url": reverse("account_logout")},
            ]
        }
    else:
        return {
            "profile_items": [
                {"name": "Login", "url": reverse("account_login")},
                {"name": "Signup", "url": reverse("account_signup")},
            ]
        }
