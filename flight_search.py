import os
import requests
from pprint import pprint
import datetime as dt

TEQUILA_ENDP = "https://tequila-api.kiwi.com/"
TEQUILA_SEARCH = "v2/search"
TEQUILA_LOC = "locations/query"
TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")

HEADERS_TEQ = {
    "apikey": TEQUILA_API_KEY
}

class FlightSearch:
    """Talking to the Flight Search API"""

    def get_iata_city_code(self, city_name: str):
        params_loc = {
            "term": city_name,
            "locale": "en-US",
            "location_types": "city",
            "limit": 1,
        }
        response_teq_loc = requests.get(url=TEQUILA_ENDP + TEQUILA_LOC, params=params_loc, headers=HEADERS_TEQ)
        response_teq_loc.raise_for_status()
        data = response_teq_loc.json()
        return data["locations"][0]["code"]

    def set_dates(self):
        date_from = (dt.date.today() + dt.timedelta(days=1)).strftime("%d/%m/%Y")
        date_to = (dt.date.today() + dt.timedelta(days=180)).strftime("%d/%m/%Y")
        return date_from, date_to

    def get_cheapest_ticket(self, city):
        params_search = {
            "fly_from": "LON",
            "fly_to": city,
            "date_from": self.set_dates()[0],
            "data_to": self.set_dates()[1],
            "curr": "AUD",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "max_stopovers": 0,
            "limit": 1,
        }
        response_teq_search = requests.get(url=TEQUILA_ENDP + TEQUILA_SEARCH, params=params_search, headers=HEADERS_TEQ)
        response_teq_search.raise_for_status()
        data = response_teq_search.json()
        return data["data"][0]['price']

#
# fs = FlightSearch()
# print(fs.get_cheapest_ticket("TYO")['price'])
