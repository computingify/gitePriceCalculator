
from datetime import date

PERIOD_PRICING = {
    "basse": 90,
    "moyenne": 130,
    "haute": 160,
}

SEASON_PERIODS = {
    "moyenne": [
        {"start": (7, 1), "end": (8, 31)},  # Juillet-Août
    ],
    "haute": [
        {"days": [(12, 24), (12, 31)]},  # 24/12 et 31/12
    ]
}

BASE_PEOPLE = 4
EXTRA_PERSON_PRICE = 15
