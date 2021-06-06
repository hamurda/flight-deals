import os
import requests
from flight_data import FlightData
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

    def cheapest_tickets(self, city):
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

        try:
            data = response_teq_search.json()[0]
        except IndexError:
            print(f"No flights found for {city}")
            return None

        ticket_details = FlightData()
        ticket_details.price = data["data"][0]['price']
        ticket_details.departure_city = data["data"][0]['cityFrom']
        ticket_details.departure_airport = data["data"][0]['flyFrom']
        ticket_details.destination_city = data["data"][0]['cityTo']
        ticket_details.destination_airport = data["data"][0]['flyTo']
        ticket_details.out_date = data["route"][0]["local_departure"].split("T")[0],
        ticket_details.return_date = data["route"][1]["local_departure"].split("T")[0]

        print(f"{ticket_details.destination_city}: {ticket_details.price}AUD")
        return ticket_details
