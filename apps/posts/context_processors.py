def posts_items(request):
    menu_items = [
        {"name": "Blog", "url": "posts:post_home"},
        {"name": "Nouveau post", "url": "posts:add_post"},
    ]
    return {"posts_items": menu_items}
