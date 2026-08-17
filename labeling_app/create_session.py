# Create a token to use in our discord generated link

#sql alchemy to increment token on each airflow run
# Can we reuse our engine or do we need to create new


import secrets
from datetime import date, datetime
from sqlalchemy import text
from ingest.db import get_engine


BREAK_ID = 'belmar'

def create_session():
    engine = get_engine()
    token = secrets.token_urlsafe(16)

    with engine.connect() as conn:
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

    return token