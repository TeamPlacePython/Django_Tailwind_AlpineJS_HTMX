def allauth_login_context(request):
    return {
        "title": "Connexion",
        "no_accout": "Si vous n’avez pas encore créé de compte, veuillez",
        "sign_up": "vous inscrire.",
    }
