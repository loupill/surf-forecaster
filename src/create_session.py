import logging
import secrets
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from sqlalchemy import text
from ingest.db import get_engine


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

BREAK_ID = 'belmar'
EASTERN = ZoneInfo("America/New_York")

def create_session():
    engine = get_engine()
    token = secrets.token_urlsafe(16)
    today_eastern = datetime.now(EASTERN).date()

    with engine.connect() as conn:
        try:
            row = (conn.execute(
                        text("""
                            select token from gold.labeling_sessions where session_date = :today_date and break_id = :break_id
                        """
                        ),
                        {
                            "today_date": today_eastern,
                            "break_id": BREAK_ID
                        }
                    )
                ).fetchone()
            if row is not None:
                return row[0]

            else:
                conn.execute(
                    text("""
                        insert into gold.labeling_sessions (token, break_id, session_date, sent_at)
                        values (:token, :break_id, :session_date, :sent_at)
                    """
                    ),
                    {
                        "token": token,
                        "break_id": BREAK_ID,
                        "session_date": today_eastern,
                        "sent_at": datetime.now(timezone.utc),
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