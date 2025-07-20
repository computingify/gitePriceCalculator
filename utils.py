
from datetime import datetime, timedelta, date
from types import SimpleNamespace
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

def calculate_price(start_date_str, end_date_str, people, isInsurence=False):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    nights = (end_date - start_date).days
    total = 0
    detail = []

    for i in range(nights):
        day = start_date + timedelta(days=i)
        discount_percentage = config.DISCOUNT_PRICE_MORE_THAN_7_NIGHTS if nights >= 7 else 0
        period = get_period(day)
        night_price = config.BASE_PRICE_PER_NIGHT * (1 + config.PERIOD_PERCENTAGE[period]) # calculate the price for the night based on the period
        night_price = night_price * (1 - discount_percentage) # Apply discount for long stays
        extra_people = max(0, (people.adult + people.children) - config.BASE_PEOPLE)
        price = round(night_price + extra_people * (config.BASE_EXTRA_PERSON_PRICE * (1 + config.PERIOD_PERCENTAGE[period])))
        total += price
        detail.append((day.strftime('%Y-%m-%d'), period, price))

    total += config.CLEANING_PRICE + (people.adult * nights * config.TAXES_PER_PERSON_NIGHT)
    total += nights * config.INSURENCE_PER_NIGHT if isInsurence else 0
    insurence = nights * config.INSURENCE_PER_NIGHT
    taxes = people.adult * nights * config.TAXES_PER_PERSON_NIGHT
    peopleNightPrice = round(total / (nights * (people.adult + people.children)), 2) if (nights * (people.adult + people.children)) > 0 else 0
    total = round(total, 2)
    return {"nights": nights, "adult": people.adult, "children": people.children, "baby": people.baby, "detail": detail, "cleaning": config.CLEANING_PRICE, "is_insurence": isInsurence, "insurence": insurence, "taxes": taxes, "total": total, "peopleNightPrice": peopleNightPrice}
