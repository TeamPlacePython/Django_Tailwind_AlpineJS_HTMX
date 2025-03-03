def members_items(request):
    menu_items = [{"name": "Team", "url": "members:member-list"}]
    if request.user.is_authenticated and request.user.is_staff:
        menu_items.extend(
            [
                {"name": "Create", "url": "members:member-create"},
                {"name": "Tableau", "url": "members:member-table"},
            ]
        )

    return {"members_items": menu_items}
