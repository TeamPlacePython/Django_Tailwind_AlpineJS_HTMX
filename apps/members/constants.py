ROLES_CHOICES = [
    ("coach", "Entraineur"),
    ("member", "Membre"),
    ("president", "Président"),
    ("treasurer", "Trésorier"),
    ("vice-president", "Vice-Président"),
    ("secretary", "Secrétaire"),
    ("web-master", "Web-master"),
    ("visitor", "Visiteur"),
    ("testman", "Testman"),
]

STATUS_CHOICES = [
    ("active", "Actif"),
    ("inactive", "Inactif"),
    ("pending", "En attente"),
]

WEAPON_CHOICES = [
    ("epee", "Épée"),
    ("fleuret", "Fleuret"),
    ("sabre", "Sabre"),
]

HANDENESS_CHOICES = [
    ("right", "Droitier"),
    ("left", "Gaucher"),
    ("ambidextrous", "Ambidextre"),
]

GENDER_CHOICES = [
    ("male", "Homme"),
    ("female", "Femme"),
    ("other", "Autre"),
]

STATUS_BADGES = {
    "active": "text-success",
    "pending": "text-warning",
    "inactive": "text-danger",
}
