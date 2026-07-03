import yaml
import logging
from pathlib import Path
from ingest.db import get_engine, write_dataframe
from ingest.marine import fetch_marine_data, prepare_marine_data
from ingest.weather import fetch_weather_data, prepare_weather_data
from ingest.tide import fetch_tide_data, format_tides
import pandas as pd
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def run_ingest(): 
    config_path = Path(__file__).parent.parent / "config" / "breaks.yml"
    with open(config_path) as f:
        breaks = yaml.safe_load(f)["breaks"]

    df_marine = pd.DataFrame()
    df_weather = pd.DataFrame()
    df_tide = pd.DataFrame()

    try:
        for b in breaks:
            lat = b["latitude"]
            lon = b["longitude"]
            logging.info(f"Fetching data for {b['name']} (lat={lat}, lon={lon})")

            marine_data = fetch_marine_data(latitude=lat, longitude=lon)
            marine_data['break_id'] = b["id"]
            marine_data['retrieved_at'] = datetime.now(timezone.utc)
            df_marine = pd.concat([df_marine, marine_data], ignore_index=True)

            weather_data = fetch_weather_data(latitude=lat, longitude=lon)
            weather_data['break_id'] = b["id"]
            weather_data['retrieved_at'] = datetime.now(timezone.utc)
            df_weather = pd.concat([df_weather, weather_data], ignore_index=True)

        # Tide data doesn't vary by break, only by station, so fetch once per
        # distinct station instead of once per break
        station_ids = {b["station_id"] for b in breaks}
        for station_id in station_ids:
            logging.info(f"Fetching tide data for station {station_id}")
            tide_data = fetch_tide_data(station_id=station_id)
            tide_data['station_id'] = station_id
            tide_data['retrieved_at'] = datetime.now(timezone.utc)
            df_tide = pd.concat([df_tide, tide_data], ignore_index=True)

        # Prep data to be written to Postgres
        df_marine = prepare_marine_data(df_marine)
        df_weather = prepare_weather_data(df_weather)
        df_tide = format_tides(df_tide)

        # Write dataframes to Postgres
        engine = get_engine()

        write_dataframe(df=df_marine, table_name='marine_forecasts', schema='raw', engine=engine)
        logging.info(f"Wrote {len(df_marine)} rows to raw.marine_forecasts")

        write_dataframe(df=df_weather, table_name='weather_forecasts', schema='raw', engine=engine)
        logging.info(f"Wrote {len(df_weather)} rows to raw.weather_forecasts")

        write_dataframe(df=df_tide, table_name='tide_forecasts', schema='raw', engine=engine)
        logging.info(f"Wrote {len(df_tide)} rows to raw.tide_forecasts")

    except Exception as e:
        logging.error(f"Ingest failed: {e}")
        raise

if __name__ == "__main__":
    run_ingest()




