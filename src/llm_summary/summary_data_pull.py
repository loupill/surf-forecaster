from ingest.db import get_engine
from sqlalchemy import text
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

scored_data = """
select *
from gold.scored_forecasts
where retrieved_at = (select max(retrieved_at) from gold.scored_forecasts)
"""

def get_data():
    '''
    Get necessary data for creating summary
    '''

    scored_data = """
    select *
    from gold.scored_forecasts
    where retrieved_at = (select max(retrieved_at) from gold.scored_forecasts)
    """

    engine = get_engine()

    with engine.connect() as conn:
        try:
            df = pd.read_sql(text(scored_data), conn)
        except Exception as e:
            logging.error(f"Read failed: {e}")
            raise

    return df



if __name__ == "__main__":
    df = get_data()

