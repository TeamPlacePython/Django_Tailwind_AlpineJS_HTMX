def history_items(request):
    menu_items = [
        {"name": "Histoire", "url": "history:history"},
    ]
    return {"history_items": menu_items}
