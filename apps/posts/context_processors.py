def posts_items(request):
    menu_items = [
        {"name": "Blog", "url": "posts:post_index"},
        {"name": "Nouveau post", "url": "posts:post_create"},
    ]
    return {"posts_items": menu_items}
