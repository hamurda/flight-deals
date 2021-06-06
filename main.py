from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager

from pprint import pprint

dm = DataManager()
fs = FlightSearch()

sheet_data = DataManager.pass_prices(dm)

for item in sheet_data:
    if item['iataCode'] == "":
        item['iataCode'] = fs.get_iata_city_code(item["city"])
        dm.update_row(item)