def messageboard_items(request):
    menu_items = [
        # {"name": "Messages", "url": "messageboard:messageboard"},
        # {"name": "Subscribe", "url": "messageboard:subscribe"},
        {"name": "Newsletter", "url": "messageboard:newsletter"},
    ]
    return {"messageboard_items": menu_items}
