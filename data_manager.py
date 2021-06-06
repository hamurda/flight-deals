import os
import requests
from pprint import pprint

SHEETY_ENDP = os.environ.get("SHEETY_ENDP")
SHEETY_ENDP_USER = os.environ.get("SHEETY_ENDP_USER")

response = requests.get(url=SHEETY_ENDP)
response.raise_for_status()
data = response.json()

class DataManager:
    """Responsible for talking to the Google Sheet"""
    def __init__(self):
        self.data = data

    def pass_destionation_data(self):
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
        print(put_response.text)

    def add_user(self):
        params_post = {
            "user": {
                'firstName': self.first_name,
                'lastName': self.last_name,
                'email': self.email,
            }
        }

        post_response = requests.post(url=SHEETY_ENDP_USER, json=params_post)
        print(post_response.text)

    def update_user(self, item):
        put_url = SHEETY_ENDP_USER + "/" + str(item['id'])
        params_put = {
            "user": {
                'firstName': item['firstName'],
                'lastName': item['lastName'],
                'email': item['email'],
            }
        }

        put_response = requests.put(url=put_url, json=params_put)
        print(put_response.text)

    def get_users(self):
        get_response = requests.get(url=SHEETY_ENDP_USER)
        get_response.raise_for_status()
        users = get_response.json()['users']
        return users
