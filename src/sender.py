"""
Sending layer
"""

from twilio.rest import Client
from src.config import Config
from src.data_reader import get_sheet_client, update_row

client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

def send_message(row, row_index, sheet):
    try:
        message = client.messages.create(
            body=row['message'],
            from_=Config.TWILIO_PHONE_NUMBER,
            to=row['mobile']
        )
        print(f"Message sent to {row['name']}: {message.sid}")
        update_row(sheet, row_index, {'status': 'Sent'})
    except Exception as e:
        print(f"Failed to send message to {row['name']}: {e}")
        update_row(sheet, row_index, {'status': 'Failed'})