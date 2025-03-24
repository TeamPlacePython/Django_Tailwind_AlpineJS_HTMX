def sport_items(request):
    menu_items = [
        {"name": "Cotisations", "url": "sport:sport_category_cotisations"},
        {"name": "Horaires", "url": "sport:sport_training_hours"},
    ]
    return {"sport_items": menu_items}
