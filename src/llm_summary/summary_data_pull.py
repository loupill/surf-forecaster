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
    select 
        forecast_time
        , wave_height_ft 
        , swell_wave_height_ft 
        , wind_wave_height_ft 
        , swell_wave_period_s 
        , wave_period_s 
        , swell_wave_direction_cardinal 
        , wave_direction_cardinal 
        , tide
        , temperature_f 
        , wind_speed_mph 
        , wind_direction_cardinal
        , surf_score
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

