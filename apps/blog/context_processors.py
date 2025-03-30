def blog_items(request):
    menu_items = [
        {"name": "Blog", "url": "blog:blog_index"},
    ]
    return {"blog_items": menu_items}
