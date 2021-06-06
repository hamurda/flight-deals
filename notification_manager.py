from twilio.rest import Client
import os
import smtplib

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

    def send_emails(self, emails, text, google_link):
        with smtplib.SMTP("smpt.gmail.com") as connection:
            connection.starttls()
            connection.login(user="", password="")
            for email in emails:
                connection.sendmail(from_addr="", to_addrs=email,
                                    msg=f"Subject:Flight Deal!\n\n{text}\n{google_link}")
