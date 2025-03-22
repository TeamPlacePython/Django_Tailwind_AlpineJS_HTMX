def members_items(request):
    # Default menu items that all users can see
    menu_items = [{"name": "Membres", "url": "members:member-list"}]

    # If the user is authenticated and is a staff member, add extra menu items
    if request.user.is_authenticated and request.user.is_staff:
        menu_items.extend(
            [
                {"name": "Création", "url": "members:member-create"},
                {"name": "Tableau", "url": "members:member-table"},
            ]
        )

    # Return the context that will be available in templates
    return {"members_items": menu_items}
