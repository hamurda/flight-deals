from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from user import User

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

    if ticket is None:
        continue

    if ticket.price < item["lowestPrice"]:

        users = dm.get_users()
        emails = [user['email'] for user in users]
        names = [user['firstName'] for user in users]

        text = f"Low price alert! Only {ticket.price}AUD to fly from {ticket.origin_city}-" \
               f"{ticket.origin_airport} to {ticket.destination_city}" \
               f"-{ticket.destination_airport}, from {ticket.out_date} to {ticket.return_date}."
        if ticket.stop_overs !=0:
            text+=f"\nFlight has {ticket.stop_overs} stop over, via {ticket.via_city[0]}"
        # NotificationManager.send_SMS(text)
        link = f"https://www.google.co.uk/flights?hl=en#flt={ticket.origin_airport}." \
               f"{ticket.destination_airport}.{ticket.out_date}*" \
               f"{ticket.destination_airport}.{ticket.origin_airport}.{ticket.return_date}"

        NotificationManager.send_emails(emails, text, link)

#------USER------
#TODO:Interface is needed for user ineraction
# us = User()
#
# is_cont = True
#
# while is_cont:
#     us.first_name = input("What is your first name?\n")
#     us.last_name = input("What is your last name?\n")
#     email = input("What is your email?\n")
#     email_ver = input("Type your email again:\n")
#
#     if email == email_ver:
#         us.email = email
#         us.add_user()
#         is_cont = False
#     else:
#         print("Emails don't match.")