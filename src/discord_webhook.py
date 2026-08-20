import logging
import requests
import os
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


discord_webhook = os.environ["DISCORD_WEBHOOK"]

def send_discord_message(message):
    payload = {"content": message }
    response = requests.post(discord_webhook, json = payload)
    if response.status_code == 204:
        logging.info("Discord message sent successfully")
    else:
        logging.error(f"Failed to send Discord message: {response.status_code}")
