import logging
import requests
import os
from dotenv import load_dotenv


load_dotenv()

discord_webhook = os.environ["DISCORD_WEBHOOK"]

payload = {"content": "This is a test message!" }

response = requests.post(discord_webhook, json = payload)

if response.status_code == 204:
    print("Message sent successfully")
else:
    print(f"Failed to send message {response.status_code}")
