def allauth_login_context(request):
    return {
        "no_accout": "Si vous n’avez pas encore créé de compte, veuillez",
        "sign_up": "vous inscrire.",
    }


def profile_items(request):
    menu_items = [
        {"name": "My profile", "url": "users:profile"},
        {"name": "Edit Profile", "url": "users:profile_edit"},
        {"name": "Settings", "url": "users:profile_settings"},
        {"name": "Log Out", "url": "account_logout"},
    ]
    return {"profile_items": menu_items}
