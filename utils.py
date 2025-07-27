
from datetime import datetime, timedelta, date
import config
import holidays
import requests
from ics import Calendar

def is_may_bridge_day(d: date):
    fr_holidays = holidays.France(years=d.year)
    # for date, name in fr_holidays.items():
    #     print(date, name)
    for holiday_date, holiday_name in fr_holidays.items():
        if holiday_name in getattr(config, "FRENCH_HOLIDAYS_MEDIUM_PRICE", set()):
            if d in [holiday_date + timedelta(days=offset) for offset in config.MEDUIM_PRICE_AROUND_HOLIDAYS]:
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

def last_minute_discount(d: date):
    today = datetime.now().date()
    if 0 <= (d - today).days < config.LAST_MINUTES_DAYS:
        return config.LAST_MUNITE_DISCOUNT
    return 0

def calculate_price(start_date_str, end_date_str, people, isInsurence=False, isExtraAccess=False):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    nights = (end_date - start_date).days
    total = 0
    detail = []
    discount_amount_more_days = 0
    discount_amount_last_minute = 0

    for i in range(nights):
        note = ""
        day = start_date + timedelta(days=i)
        period = get_period(day)
        night_price = config.BASE_PRICE_PER_NIGHT * (1 + config.PERIOD_PERCENTAGE[period]) # calculate the price for the night based on the period
        extra_people = max(0, (people.adult + people.children) - config.BASE_PEOPLE)
        price = night_price + extra_people * (config.BASE_EXTRA_PERSON_PRICE * (1 + config.PERIOD_PERCENTAGE[period]))
        
        discount_percentage_7d = config.DISCOUNT_PRICE_MORE_THAN_7_NIGHTS if i >= 7 else 0
        discount_amount_more_days += price * discount_percentage_7d
        if discount_percentage_7d > 0:
            note = f"Réduc +7 nuits (-{round(price * discount_percentage_7d, 2)} €)"
        price = price * (1- discount_percentage_7d) # Apply discount for long stays
        
        discount_amount_last_minute += price * last_minute_discount(day)
        if last_minute_discount(day) > 0:
            note = f"Réduc dernière minute (-{round(price * last_minute_discount(day), 2)} €)"
        price = price * (1 - last_minute_discount(day))  # Apply last minute discount if applicable
        
        total += price
        detail.append((day.strftime('%d-%m-%Y'), period, round(price, 2), note))

    total += config.CLEANING_PRICE + (people.adult * nights * config.TAXES_PER_PERSON_NIGHT)
    total += nights * config.INSURENCE_PER_NIGHT if isInsurence else 0
    extra_access_amount = nights * config.EXTRA_ACCESS_PRICE if isExtraAccess else 0
    total += extra_access_amount
    insurence = nights * config.INSURENCE_PER_NIGHT
    taxes = people.adult * nights * config.TAXES_PER_PERSON_NIGHT
    peopleNightPrice = total / (nights * (people.adult + people.children)) if (nights * (people.adult + people.children)) > 0 else 0
    return {
        "nights": nights,
        "adult": people.adult,
        "children": people.children,
        "baby": people.baby,
        "detail": detail,
        "cleaning": config.CLEANING_PRICE,
        "extra_access_amount": round(extra_access_amount, 2),
        "is_insurence": isInsurence,
        "insurence": round(insurence, 2),
        "taxes": round(taxes, 2),
        "total": round(total, 2),
        "discount_amount_more_days": round(discount_amount_more_days, 2),
        "discount_amount_last_minute": round(discount_amount_last_minute, 2),
        "peopleNightPrice": round(peopleNightPrice, 2)
        }
