import unittest
from datetime import date, timedelta
import utils

from unittest.mock import patch, MagicMock
import utils

class DummyConfig:
    PERIOD_PERCENTAGE = {"basse": 0, "moyenne": 0.16, "haute": 0.56}
    SEASON_PERIODS = {
        "moyenne": [{"start": (7, 1), "end": (8, 31)}],
        "haute": [{"days": [(12, 24), (12, 25), (12, 31), (1, 1)]}]
    }
    FRENCH_HOLIDAYS_MEDIUM_PRICE = {"Lundi de Pentecôte"}
    MEDUIM_PRICE_AROUND_HOLIDAYS = (-1, 0, 1)
    BASE_PRICE_PER_NIGHT = 100
    BASE_PEOPLE = 6
    BASE_EXTRA_PERSON_PRICE = 20
    CLEANING_PRICE = 60
    INSURENCE_PER_NIGHT = 10
    TAXES_PER_PERSON_NIGHT = 1
    DISCOUNT_PRICE_MORE_THAN_7_NIGHTS = 0.1
    LAST_MINUTES_DAYS = 3
    LAST_MUNITE_DISCOUNT = 0.20
    EXTRA_ACCESS_PRICE = 20

class DummyPeople:
    def __init__(self, adult, children, baby):
        self.adult = adult
        self.children = children
        self.baby = baby
        
@patch.object(utils, 'config', DummyConfig)
class TestUtils(unittest.TestCase):

    # Attention: Cette fonction retourne True si le jour est un jour férié ou un jour de pont
    # mais également pour le jours avant et après le jour férié 
    def test_is_may_bridge_day(self):
        # Test avec un jour férié connu
        d = date(2025, 6, 9)  # Lundi de Pentecôte
        self.assertTrue(utils.is_may_bridge_day(d))
        # Test avec un jour non férié mais dans le jour après, qui est aussi en tarif suppérieur
        d = date(2025, 6, 10)
        self.assertTrue(utils.is_may_bridge_day(d))
        # Test avec un jour non férié mais dans le jour avant, qui est aussi en tarif suppérieur
        d = date(2025, 6, 8)
        self.assertTrue(utils.is_may_bridge_day(d))
        # Test avec un jour non férié
        d = date(2025, 6, 6)
        self.assertFalse(utils.is_may_bridge_day(d))

    def test_get_period(self):
        # Test haute saison (Noël)
        d = date(2025, 12, 25)
        self.assertEqual(utils.get_period(d), "haute")
        # Test moyenne saison (juillet)
        d = date(2025, 7, 10)
        self.assertEqual(utils.get_period(d), "moyenne")
        # Test basse saison
        d = date(2025, 3, 10)
        self.assertEqual(utils.get_period(d), "basse")

    def test_last_minute_discount(self):
        today = date.today()
        d = today + timedelta(days=3)
        discount = utils.last_minute_discount(d)
        self.assertIn(discount, [0, utils.config.LAST_MUNITE_DISCOUNT])

    def test_calculate_price_basic_low(self):
        nb_adults = 2
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price("2025-02-01", "2025-02-04", people)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], 3)
        self.assertEqual(result["adult"], 2)
        self.assertIn("total", result)
        self.assertEqual(result["total"], 3 * utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE["basse"]) + utils.config.CLEANING_PRICE + nb_adults * 3 * utils.config.TAXES_PER_PERSON_NIGHT)
    
    def test_calculate_price_basic_medium(self):
        nb_adults = 2
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price("2025-07-01", "2025-07-04", people)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], 3)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        self.assertEqual(
            result["total"],
            3 * utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE["moyenne"])
            + utils.config.CLEANING_PRICE
            + nb_adults * 3 * utils.config.TAXES_PER_PERSON_NIGHT
        )
    
    def test_calculate_price_basic_high(self):
        nb_adults = 2
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price("2025-12-24", "2025-12-26", people)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], 2)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        self.assertEqual(
            result["total"],
            2 * utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE["haute"])
            + utils.config.CLEANING_PRICE
            + nb_adults * 2 * utils.config.TAXES_PER_PERSON_NIGHT
        )
    
    def test_calculate_price_chrismas(self):
        nb_adults = 2
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price("2025-12-24", "2025-12-27", people)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], 3)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        self.assertEqual(
            result["total"],
            2 * utils.config.BASE_PRICE_PER_NIGHT * (1 + utils.config.PERIOD_PERCENTAGE["haute"])
            + utils.config.BASE_PRICE_PER_NIGHT * (1 + utils.config.PERIOD_PERCENTAGE["basse"])
            + utils.config.CLEANING_PRICE
            + nb_adults * 3 * utils.config.TAXES_PER_PERSON_NIGHT
        )

    def test_calculate_price_with_insurence(self):
        nb_adults = 2
        nb_nights = 3
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price("2025-02-01", "2025-02-04", people, isInsurence=True)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        self.assertEqual(
            result["total"],
            nb_nights * utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE["basse"])
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
            + nb_nights * utils.config.INSURENCE_PER_NIGHT
        )

    def test_calculate_price_with_extra(self):
        nb_adults = 2
        nb_nights = 3
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price("2025-02-01", "2025-02-04", people, isExtraAccess=True)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        self.assertEqual(
            result["total"],
            nb_nights * utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE["basse"])
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
            + nb_nights * utils.config.EXTRA_ACCESS_PRICE
        )

    def test_calculate_price_with_more_people(self):
        nb_adults = 8
        nb_nights = 3
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price("2025-02-01", "2025-02-04", people)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        self.assertEqual(
            result["total"],
            nb_nights * utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE["basse"])
            + (nb_adults - utils.config.BASE_PEOPLE) * nb_nights * utils.config.BASE_EXTRA_PERSON_PRICE
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
        )

    def test_calculate_price_with_more_people_medium(self):
        nb_adults = 8
        nb_nights = 3
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price("2025-08-01", "2025-08-04", people)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        self.assertEqual(
            result["total"],
            nb_nights * utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE["moyenne"])
            + (nb_adults - utils.config.BASE_PEOPLE) * nb_nights * (utils.config.BASE_EXTRA_PERSON_PRICE*(1+utils.config.PERIOD_PERCENTAGE["moyenne"]))
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
        )

    def test_calculate_price_with_more_people_and_children(self):
        nb_adults = 8
        nb_children = 8
        nb_nights = 3
        people = DummyPeople(adult=nb_adults, children=nb_children, baby=0)
        result = utils.calculate_price("2025-02-01", "2025-02-04", people)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        self.assertEqual(
            result["total"],
            nb_nights * utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE["basse"])
            + (nb_adults + nb_children - utils.config.BASE_PEOPLE) * nb_nights * utils.config.BASE_EXTRA_PERSON_PRICE
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
        )

    def test_calculate_price_with_more_people_and_children_baby(self):
        nb_adults = 8
        nb_children = 8
        nb_baby = 4
        nb_nights = 3
        people = DummyPeople(adult=nb_adults, children=nb_children, baby=nb_baby)
        result = utils.calculate_price("2025-02-01", "2025-02-04", people)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        self.assertEqual(
            result["total"],
            nb_nights * utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE["basse"])
            + (nb_adults + nb_children - utils.config.BASE_PEOPLE) * nb_nights * utils.config.BASE_EXTRA_PERSON_PRICE
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
        )

    def test_calculate_price_last_minutes_simple(self):
        nb_adults = 10
        nb_nights = 3
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price(
            date.today().strftime('%Y-%m-%d'),
            (date.today() + timedelta(days=3)).strftime('%Y-%m-%d'),
            people)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        
        night = utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE[utils.get_period(date.today())])
        extra_people = (nb_adults - utils.config.BASE_PEOPLE) * utils.config.BASE_EXTRA_PERSON_PRICE *(1+utils.config.PERIOD_PERCENTAGE[utils.get_period(date.today())])
        night_extra_people = night + extra_people
        last_minute = night_extra_people* (1 - utils.config.LAST_MUNITE_DISCOUNT)
        total_night = last_minute * nb_nights
        
        self.assertEqual(
            result["total"],
            total_night
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
        )
        
        self.assertEqual(
            result["discount_amount_last_minute"],
            round(night_extra_people * 3 - last_minute * 3, 2)
        )

    def test_calculate_price_last_minutes_4days(self):
        nb_adults = 10
        nb_nights = 4
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price(
            date.today().strftime('%Y-%m-%d'),
            (date.today() + timedelta(days=4)).strftime('%Y-%m-%d'),
            people)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        
        night = utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE[utils.get_period(date.today())])
        extra_people = (nb_adults - utils.config.BASE_PEOPLE) * utils.config.BASE_EXTRA_PERSON_PRICE *(1+utils.config.PERIOD_PERCENTAGE[utils.get_period(date.today())])
        night_extra_people = night + extra_people
        last_minute = night_extra_people * (1 - utils.config.LAST_MUNITE_DISCOUNT)
        total_night = last_minute * 3 + night_extra_people
        
        self.assertEqual(
            result["total"],
            total_night
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
        )
        
    def test_calculate_price_more_than_7days(self):
        nb_adults = 10
        nb_nights = 10
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price(
            "2025-02-01",
            "2025-02-11",
            people)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        
        night = utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE["basse"])
        extra_people = (nb_adults - utils.config.BASE_PEOPLE) * utils.config.BASE_EXTRA_PERSON_PRICE *(1+utils.config.PERIOD_PERCENTAGE["basse"])
        night_extra_people = night + extra_people
        seven_days = night_extra_people* (1 - utils.config.DISCOUNT_PRICE_MORE_THAN_7_NIGHTS)
        total_night = night_extra_people * 7 + seven_days * (nb_nights - 7)
        
        self.assertEqual(
            result["total"],
            total_night
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
        )
        
        self.assertEqual(
            result["discount_amount_more_days"],
            night_extra_people * (nb_nights - 7) - seven_days * (nb_nights - 7)  # Total price without discount - price with discount
        )
        
    def test_calculate_price_last_minutes_and_more_than_7days(self):
        nb_adults = 10
        nb_nights = 10
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price(
            date.today().strftime('%Y-%m-%d'),
            (date.today() + timedelta(days=nb_nights)).strftime('%Y-%m-%d'),
            people)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        
        night = utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE[utils.get_period(date.today())])
        extra_people = (nb_adults - utils.config.BASE_PEOPLE) * utils.config.BASE_EXTRA_PERSON_PRICE *(1+utils.config.PERIOD_PERCENTAGE[utils.get_period(date.today())])
        night_extra_people = night + extra_people
        
        seven_days = night_extra_people* (1 - utils.config.DISCOUNT_PRICE_MORE_THAN_7_NIGHTS)
        last_minute = night_extra_people * (1 - utils.config.LAST_MUNITE_DISCOUNT)
        
        total_night = last_minute * utils.config.LAST_MINUTES_DAYS + night_extra_people * (7 - utils.config.LAST_MINUTES_DAYS) + seven_days * (nb_nights - 7)
        
        self.assertEqual(
            result["total"],
            total_night
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
        )
        
        self.assertEqual(
            result["discount_amount_more_days"],
            round(night_extra_people * (nb_nights - 7) - seven_days * (nb_nights - 7), 2)
        )
        
        self.assertEqual(
            result["discount_amount_last_minute"],
            round(night_extra_people * 3 - last_minute * 3, 2)
        )
        
    def test_calculate_price_last_minutes_with_insurence(self):
        nb_adults = 10
        nb_nights = 3
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price(
            date.today().strftime('%Y-%m-%d'),
            (date.today() + timedelta(days=nb_nights)).strftime('%Y-%m-%d'),
            people, isInsurence=True)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        
        night = utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE[utils.get_period(date.today())])
        extra_people = (nb_adults - utils.config.BASE_PEOPLE) * utils.config.BASE_EXTRA_PERSON_PRICE *(1+utils.config.PERIOD_PERCENTAGE[utils.get_period(date.today())])
        night_extra_people = night + extra_people
        last_minute = night_extra_people* (1 - utils.config.LAST_MUNITE_DISCOUNT)
        total_night = last_minute * nb_nights
        
        self.assertEqual(
            result["total"],
            total_night
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
            + nb_nights * utils.config.INSURENCE_PER_NIGHT
        )
        
    def test_calculate_price_last_minutes_with_extra(self):
        nb_adults = 10
        nb_nights = 3
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price(
            date.today().strftime('%Y-%m-%d'),
            (date.today() + timedelta(days=nb_nights)).strftime('%Y-%m-%d'),
            people, isExtraAccess=True)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        
        night = utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE[utils.get_period(date.today())])
        extra_people = (nb_adults - utils.config.BASE_PEOPLE) * utils.config.BASE_EXTRA_PERSON_PRICE *(1+utils.config.PERIOD_PERCENTAGE[utils.get_period(date.today())])
        night_extra_people = night + extra_people
        last_minute = night_extra_people* (1 - utils.config.LAST_MUNITE_DISCOUNT)
        total_night = last_minute * nb_nights
        
        self.assertEqual(
            result["total"],
            total_night
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
            + nb_nights * utils.config.EXTRA_ACCESS_PRICE
        )
        
    def test_calculate_price_more_than_7days_with_insurence(self):
        nb_adults = 10
        nb_nights = 10
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price(
            "2025-02-01",
            "2025-02-11",
            people,
            isInsurence=True)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        
        night = utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE["basse"])
        extra_people = (nb_adults - utils.config.BASE_PEOPLE) * utils.config.BASE_EXTRA_PERSON_PRICE *(1+utils.config.PERIOD_PERCENTAGE["basse"])
        night_extra_people = night + extra_people
        seven_days = night_extra_people* (1 - utils.config.DISCOUNT_PRICE_MORE_THAN_7_NIGHTS)
        total_night = night_extra_people * 7 + seven_days * (nb_nights - 7)
        
        self.assertEqual(
            result["total"],
            total_night
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
            + nb_nights * utils.config.INSURENCE_PER_NIGHT
        )
        
    def test_calculate_price_more_than_7days_with_extra(self):
        nb_adults = 10
        nb_nights = 10
        people = DummyPeople(adult=nb_adults, children=0, baby=0)
        result = utils.calculate_price(
            "2025-02-01",
            "2025-02-11",
            people,
            isExtraAccess=True)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["nights"], nb_nights)
        self.assertEqual(result["adult"], nb_adults)
        self.assertIn("total", result)
        
        night = utils.config.BASE_PRICE_PER_NIGHT*(1+utils.config.PERIOD_PERCENTAGE["basse"])
        extra_people = (nb_adults - utils.config.BASE_PEOPLE) * utils.config.BASE_EXTRA_PERSON_PRICE *(1+utils.config.PERIOD_PERCENTAGE["basse"])
        night_extra_people = night + extra_people
        seven_days = night_extra_people* (1 - utils.config.DISCOUNT_PRICE_MORE_THAN_7_NIGHTS)
        total_night = night_extra_people * 7 + seven_days * (nb_nights - 7)
        
        self.assertEqual(
            result["total"],
            total_night
            + utils.config.CLEANING_PRICE
            + nb_adults * nb_nights * utils.config.TAXES_PER_PERSON_NIGHT
            + nb_nights * utils.config.EXTRA_ACCESS_PRICE
        )
    

if __name__ == "__main__":
    unittest.main()