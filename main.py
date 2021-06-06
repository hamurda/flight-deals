from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager

from pprint import pprint

dm = DataManager()
fs = FlightSearch()

sheet_data = DataManager.pass_destionation_data(dm)

for item in sheet_data:
    if item['iataCode'] == "":
        item['iataCode'] = fs.get_iata_city_code(item["city"])
        dm.update_row(item)

sheet_data = DataManager.pass_destionation_data(dm)
for item in sheet_data:
    cost = fs.get_cheapest_ticket(item['iataCode'])
    if item["lowestPrice"] > cost:
        item["lowestPrice"] = cost
        dm.update_row(item)
    print(f"{item['city']}: {item['lowestPrice']}")