def images_items(request):
    menu_items = [
        {"name": "Mur d'image", "url": "images:image_wall"},
    ]
    return {"images_items": menu_items}
