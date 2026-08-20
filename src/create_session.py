import logging
import secrets
from datetime import date, datetime
from sqlalchemy import text
from ingest.db import get_engine


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

BREAK_ID = 'belmar'

def create_session():
    engine = get_engine()
    token = secrets.token_urlsafe(16)

    with engine.connect() as conn:
        try:
            conn.execute(
                text("""
                    insert into gold.labeling_sessions (token, break_id, session_date, sent_at)
                    values (:token, :break_id, :session_date, :sent_at)
                """
                ),
                {
                    "token": token,
                    "break_id": BREAK_ID,
                    "session_date": date.today(),
                    "sent_at": datetime.now(),
                }
            )

            conn.commit()
            logging.info("Data written")
        except Exception as e:
            logging.error(f"Write failed: {e}")
            raise

    return token

if __name__ == "__main__":
    create_session()