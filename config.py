# Pourcentage d'augmentation des prix par rapport au BASE_PRICE_PER_NIGHT par période
PERIOD_PERCENTAGE = {
    "basse": 0,
    "moyenne": 0.16,
    "haute": 0.56,
}

# Définition des périodes
SEASON_PERIODS = {
#   "basse" -> Tout le reste de l'année
    "moyenne": [
        {"start": (7, 1), "end": (8, 31)},  # Juillet-Août
        # FRENCH_HOLIDAYS_MEDIUM_PRICE -> Jours fériés
    ],
    "haute": [
        {"days": [(12, 24), (12, 25), (12, 31), (1, 1)]},  # 24 - 25 /12 et 31/12 - 1/1
    ]
}

# Jours fériés en France où on applique un tarif plus important, doivent être les noms de jours fériés de la lib holidays 
FRENCH_HOLIDAYS_MEDIUM_PRICE = {
    # "Jour de l'an",
    # "Lundi de Pâques",
    "Lundi de Pentecôte",
    "Fête du Travail",
    "Fête de la Victoire",
    "Ascension",
    # "Fête nationale",
    # "Assomption",
    # "Toussaint",
    # "Armistice",
    # "Noël",
}
MEDUIM_PRICE_AROUND_HOLIDAYS = (-1, 0, 1)  # Jours avant et après les jours fériés sont à tarif moyen

# Configuration des prix
BASE_PRICE_PER_NIGHT = 320 # Prix de base par nuit
BASE_PEOPLE = 6 # Nombre de personnes inclus dans le tarif de base
BASE_EXTRA_PERSON_PRICE = 20 # Prix de base par personne supplémentaire
CLEANING_PRICE = 80 # Frais de ménage par séjour
INSURENCE_PER_NIGHT = 6 # Frais d'assurance en € par nuit
TAXES_PER_PERSON_NIGHT = 1 # Taxe de séjour en € par adulte et par nuit
DISCOUNT_PRICE_MORE_THAN_7_NIGHTS = 0.07 # Pourcentage de réduction si 7 nuits ou plus (7%)
LAST_MINUTES_DAYS = 3 # Nombre de jours pour considérer une réservation comme de dernière minute
LAST_MUNITE_DISCOUNT = 0.20 # Pourcentage de réduction pour les réservations de dernière minute (moins de 3 jours avant le séjour)
EXTRA_ACCESS_PRICE = 40 # Prix pour l'accès à l'espace Grenier