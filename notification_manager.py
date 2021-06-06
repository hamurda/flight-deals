from twilio.rest import Client
import os

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")


class NotificationManager:
    """Class responsibsle for sending notifications with the deal flight details"""

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_SMS(self, text):
        message = self.client.messages.create(
            body=text,
            from_="",
            to=""
        )
        print(message.sid)
