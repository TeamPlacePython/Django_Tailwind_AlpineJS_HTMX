def sport_items(request):
    menu_items = [
        {"name": "Cotisations", "url": "sport:sport_category_cotisations"},
        {"name": "Horaires", "url": "sport:training_hours"},
        {"name": "Résultats", "url": "sport:results_event_list"},
    ]
    return {"sport_items": menu_items}
