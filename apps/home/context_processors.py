def home_items(request):
    menu_items = [
        {"name": "Home", "url": "home:home-index"},
        {"name": "Résultats", "url": "home:results_list"},
    ]
    return {"home_items": menu_items}


def login_signup_items(request):
    menu_items = [
        {"name": "Login", "url": "account_login"},
        {"name": "Signup", "url": "account_signup"},
    ]
    return {"login_signup_items": menu_items}
