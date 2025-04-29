def posts_items(request):
    menu_items = [
        {"name": "Blog", "url": "posts:post_home"},
        {"name": "Nouveau post", "url": "posts:add_post"},
        {"name": "Mur d'image", "url": "posts:image_wall"},
    ]
    return {"posts_items": menu_items}
