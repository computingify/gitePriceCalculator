
from datetime import datetime, timedelta, date
from config import PERIOD_PRICING, SEASON_PERIODS, BASE_PEOPLE, EXTRA_PERSON_PRICE

def is_may_bridge_day(d: date):
    if d.month != 5:
        return False
    jours_feries = [(5, 1), (5, 8), (5, 21)]
    if (d.month, d.day) in jours_feries:
        return True
    for month, day in jours_feries:
        jour_ferie = date(d.year, month, day)
        if jour_ferie.weekday() == 3 and d == jour_ferie + timedelta(days=1):
            return True
    return False

def get_period(d: date):
    for p in SEASON_PERIODS.get("haute", []):
        if "days" in p and (d.month, d.day) in p["days"]:
            return "haute"
    for p in SEASON_PERIODS.get("moyenne", []):
        start = date(d.year, *p["start"])
        end = date(d.year, *p["end"])
        if start <= d <= end:
            return "moyenne"
    if is_may_bridge_day(d):
        return "moyenne"
    return "basse"

def calculate_price(start_date_str, end_date_str, people, cleaning_fee, tourist_tax):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    nights = (end_date - start_date).days
    total = 0
    detail = []

    for i in range(nights):
        day = start_date + timedelta(days=i)
        period = get_period(day)
        base_price = PERIOD_PRICING[period]
        extra_people = max(0, people - BASE_PEOPLE)
        price = base_price + extra_people * EXTRA_PERSON_PRICE
        total += price
        detail.append((day.strftime('%Y-%m-%d'), period, price))

    total += cleaning_fee + tourist_tax
    return {"nights": nights, "detail": detail, "total": total}
