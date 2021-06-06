from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

DEPARTURE_CITY_CODE = "LON"

dm = DataManager()
fs = FlightSearch()

sheet_data = DataManager.pass_destionation_data(dm)

for item in sheet_data:
    if item['iataCode'] == "":
        item['iataCode'] = fs.get_iata_city_code(item["city"])
        dm.update_row(item)

sheet_data = DataManager.pass_destionation_data(dm)
for item in sheet_data:
    ticket = fs.cheapest_tickets(DEPARTURE_CITY_CODE, item['iataCode'])
    if ticket.price < item["lowestPrice"]:
        text = f"Low price alert! Only {ticket.price}AUD to fly from {ticket.origin_city}-" \
               f"{ticket.origin_airport} to {ticket.destination_city}" \
               f"-{ticket.destination_airport}, from {ticket.out_date} to {ticket.return_date}."
        NotificationManager.send_SMS(text)