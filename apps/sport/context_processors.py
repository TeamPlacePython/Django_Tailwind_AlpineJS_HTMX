def sport_items(request):
    menu_items = [
        {"name": "Cotisations", "url": "sport:sport_category_cotisations"},
        {"name": "Horaires", "url": "sport:sport_training_hours"},
        {"name": "Résultats", "url": "sport:results_list"},
    ]
    return {"sport_items": menu_items}
