
from datetime import date

PERIOD_PERCENTAGE = {
    "basse": 0,
    "moyenne": 15,
    "haute": 25,
}

SEASON_PERIODS = {
    "moyenne": [
        {"start": (7, 1), "end": (8, 31)},  # Juillet-Août
    ],
    "haute": [
        {"days": [(12, 24), (12, 31)]},  # 24/12 et 31/12
    ]
}

BASE_PEOPLE = 4 # Nombre de personnes inclus dans le tarif de base
BASE_PRICE_PER_NIGHT = 220 # Prix de base par nuit
BASE_EXTRA_PERSON_PRICE = 15 # Prix par personne supplémentaire
CLEANING_PRICE = 60 # Frais de ménage par séjour
INSURENCE_PER_NIGHT = 7 # Frais d'assurance par nuit
TAXES_PER_PERSON_NIGHT = 1 # Taxe de séjour par personne et par nuit
