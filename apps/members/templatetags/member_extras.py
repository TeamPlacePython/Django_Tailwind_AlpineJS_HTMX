# app/templatetags/member_extras.py
from django import template

register = template.Library()


@register.inclusion_tag("members/partials/member_info.html")
def member_info(label, value, href=None):
    """
    Renders a member's information within a specified template.

    This inclusion tag renders the 'member_info' template with the provided label, value, and an optional link.

    Args:
        label (str): The label for the member information.
        value (str): The value to display for the member.
        href (str, optional): An optional URL to link the value to. Defaults to None.

    Returns:
        dict: A dictionary containing the label, value, and href (if provided) to pass to the template.
    """
    return {
        "label": label,
        "value": value,
        "href": href,
    }
