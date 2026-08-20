from create_session import create_session
from discord_webhook import send_discord_message
import os
import os
from dotenv import load_dotenv

load_dotenv()


def send_daily_labeling_reminder():
    base_url = os.environ["APP_BASE_URL"]
    token = create_session()
    link = f"{base_url}/rate/{token}"
    message = f"Don't forget to rate today's surf {link}"
    send_discord_message(message = message)

if __name__ == "__main__":
    send_daily_labeling_reminder()