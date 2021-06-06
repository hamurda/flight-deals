import os
import requests
from pprint import pprint

TEQUILA_ENDP = "https://tequila-api.kiwi.com/"
TEQUILA_SEARCH = "v2/search"
TEQUILA_LOC = "locations/query"
TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")

HEADERS_TEQ = {
    "apikey": TEQUILA_API_KEY
}

params_loc = {
    "term": "paris",
    "locale": "en-US",
    "location_types": "city",
    "limit": 1,
}

class FlightSearch:
    """Talking to the Flight Search API"""
    def __init__(self):
        pass


    def get_iata_city_code(self, city_name: str):
        params_loc["term"] = city_name
        response_teq_loc = requests.get(url=TEQUILA_ENDP + TEQUILA_LOC, params=params_loc, headers=HEADERS_TEQ)
        response_teq_loc.raise_for_status()
        data = response_teq_loc.json()
        return data["locations"][0]["code"]




