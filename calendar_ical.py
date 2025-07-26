import requests
from ics import Calendar
from typing import List, Dict
from datetime import datetime, timedelta

class CalendarIcal:
    def __init__(self, url: str):
        self.url = url

    def get_reserved_dates(self) -> List[Dict[str, str]]:
        """
        Retourne une liste de réservations existantes depuis un fichier .ics.
        Chaque réservation est un dict avec 'start', 'end', 'description'.
        """
        ics_request = requests.get(self.url)
        ics_request.raise_for_status()
        c = Calendar(ics_request.text)
        reserved_dates = set()
        for event in c.events:
            start = event.begin.date()
            end = event.end.date()
            current = start
            while current < end:  # end est la date de départ du client, donc non incluse
                reserved_dates.add(current.strftime('%Y-%m-%d'))
                current += timedelta(days=1)
        return sorted(reserved_dates)
