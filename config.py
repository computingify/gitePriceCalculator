
from datetime import date

PERIOD_PERCENTAGE = {
    "basse": 0,
    "moyenne": 0.16,
    "haute": 0.56,
}

SEASON_PERIODS = {
    "moyenne": [
        {"start": (7, 1), "end": (8, 31)},  # Juillet-Août
    ],
    "haute": [
        {"days": [(12, 24), (12, 31)]},  # 24/12 et 31/12
    ]
}

BASE_PRICE_PER_NIGHT = 250 # Prix de base par nuit
BASE_PEOPLE = 6 # Nombre de personnes inclus dans le tarif de base
BASE_EXTRA_PERSON_PRICE = 20 # Prix par personne supplémentaire
CLEANING_PRICE = 60 # Frais de ménage par séjour
INSURENCE_PER_NIGHT = 6 # Frais d'assurance par nuit
TAXES_PER_PERSON_NIGHT = 1 # Taxe de séjour par personne et par nuit
DISCOUNT_PRICE_MORE_THAN_7_NIGHTS = 0.07 # Réduction de 7% si 7 nuits ou plus
