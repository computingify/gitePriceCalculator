
from datetime import datetime, timedelta, date
import config

def is_may_bridge_day(d: date):
    if d.month != 5:
        return False
    jours_feries = [(5, 1), (5, 8)]
    if (d.month, d.day) in jours_feries:
        return True
    for month, day in jours_feries:
        jour_ferie = date(d.year, month, day)
        if jour_ferie.weekday() == 3 and d == jour_ferie + timedelta(days=1):
            return True
    return False

def get_period(d: date):
    for p in config.SEASON_PERIODS.get("haute", []):
        if "days" in p and (d.month, d.day) in p["days"]:
            return "haute"
    for p in config.SEASON_PERIODS.get("moyenne", []):
        start = date(d.year, *p["start"])
        end = date(d.year, *p["end"])
        if start <= d <= end:
            return "moyenne"
    if is_may_bridge_day(d):
        return "moyenne"
    return "basse"

def calculate_price(start_date_str, end_date_str, people):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    nights = (end_date - start_date).days
    total = 0
    detail = []

    for i in range(nights):
        day = start_date + timedelta(days=i)
        period = get_period(day)
        night_price = config.BASE_PRICE_PER_NIGHT * (1 + config.PERIOD_PERCENTAGE[period])
        extra_people = max(0, people - config.BASE_PEOPLE)
        price = night_price + extra_people * (config.BASE_EXTRA_PERSON_PRICE * (1 + config.PERIOD_PERCENTAGE[period]))
        total += price
        detail.append((day.strftime('%Y-%m-%d'), period, price))

    total += config.CLEANING_PRICE + (nights * config.INSURENCE_PER_NIGHT) + (people * nights * config.TAXES_PER_PERSON_NIGHT)
    return {"nights": nights, "detail": detail, "cleaning": config.CLEANING_PRICE, "insurence" : (nights * config.INSURENCE_PER_NIGHT), "taxes" : (people * nights * config.TAXES_PER_PERSON_NIGHT), "total": total}
