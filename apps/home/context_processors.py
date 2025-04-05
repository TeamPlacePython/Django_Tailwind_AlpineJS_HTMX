def home_items(request):
    menu_items = [
        {"name": "Accueil", "url": "home:home_index"},
    ]
    return {"home_items": menu_items}


def login_signup_items(request):
    menu_items = [
        {"name": "Login", "url": "account_login"},
        {"name": "Signup", "url": "account_signup"},
    ]
    return {"login_signup_items": menu_items}
