ROLES_CHOICES = [
    ("president", "Président"),
    ("vice-president", "Vice-Président"),
    ("treasurer", "Trésorier"),
    ("secretary", "Secrétaire"),
    ("coach", "Maître d'armes"),
    ("member", "Membre"),
    ("web-master", "Web-master"),
    ("testman", "Testman"),
]

STATUS_CHOICES = [
    ("active", "Actif"),
    ("pending", "En attente"),
    ("inactive", "Inactif"),
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
