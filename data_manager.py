import os
import requests
from pprint import pprint

SHEETY_ENDP = os.environ.get("SHEETY_ENDP")

response = requests.get(url=SHEETY_ENDP)
response.raise_for_status()
data = response.json()

class DataManager:
    """Responsible for talking to the Google Sheet"""
    def __init__(self):
        self.data = data

    def pass_prices(self):
        return self.data['prices']

    def update_row(self, item):
        put_url = SHEETY_ENDP + "/" + str(item['id'])
        params_put = {
            "price": {
                'city': item['city'],
                'iataCode': item['iataCode'],
                'lowestPrice': item['lowestPrice'],
                'id': item['id']}
        }
        put_response = requests.put(url=put_url, json=params_put)
        put_response.raise_for_status()