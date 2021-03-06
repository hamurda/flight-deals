import os
import requests
from flight_data import FlightData
import datetime as dt
from pprint import pprint

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

    def cheapest_tickets(self, from_city, to_city):
        params_search = {
            "fly_from": from_city,
            "fly_to": to_city,
            "date_from": self.set_dates()[0],
            "data_to": self.set_dates()[1],
            "curr": "AUD",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "max_stopovers": 2,
            "limit": 1,
        }
        response_teq_search = requests.get(url=TEQUILA_ENDP + TEQUILA_SEARCH, params=params_search, headers=HEADERS_TEQ)
        response_teq_search.raise_for_status()

        try:
            data = response_teq_search.json()["data"][0]
        except IndexError:
            print(f"No flights found for {to_city}")
            return None
        else:
            ticket_details = FlightData()
            ticket_details.price = data['price']
            ticket_details.departure_city = data['cityFrom']
            ticket_details.departure_airport = data['flyFrom']
            ticket_details.destination_city = data['cityTo']
            ticket_details.destination_airport = data['flyTo']
            ticket_details.out_date = data["local_departure"].split("T")[0],
            ticket_details.return_date = data["local_arrival"].split("T")[0],
            ticket_details.stop_overs = (len(data['route'])/2)-1
            ticket_details.via_city = data['route'][0]['cityTo']

            print(f"{ticket_details.destination_city}: {ticket_details.price}AUD")
            return ticket_details


fs = FlightSearch()
fs.cheapest_tickets("LON", "DPS")
