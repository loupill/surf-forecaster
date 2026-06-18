import requests
import pandas as pd

def fetch_marine_data(
        latitude,  
        longitude, 
        hourly = ("wave_height", "swell_wave_height", "swell_wave_period", "swell_wave_direction", "wind_wave_height", "wave_period", "wave_direction"),
        timezone = "America/New_York", 
        forecast_days = 7, 
        url = 'https://marine-api.open-meteo.com/v1/marine' 
    ):
    """
    Pull data from marine API and extract hourly data
        - Wave height
        - Swell wave height
        - Swell wave period
        - Swell wave direction
        - Wind wave height
        - Wind wave period
        - Wind wave direction
    """
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': hourly,
        'timezone': timezone,
        'forecast_days': forecast_days
    }

    response = requests.get(url, params = params)
    response.raise_for_status()
    data = response.json()
    marine_data = pd.DataFrame(data['hourly'])

    return marine_data

def prepare_marine_data(df):
    '''
    Rename columns to prepare for ingestion into database
    '''
    df = df.copy()
    df = df.rename(columns={
    "time": "forecast_time",
    "wave_height": "wave_height_m",
    "swell_wave_height": "swell_wave_height_m",
    "swell_wave_period": "swell_wave_period_s",
    "swell_wave_direction": "swell_wave_direction_deg",
    "wind_wave_height": "wind_wave_height_m",
    "wave_period": "wave_period_s",
    "wave_direction": "wave_direction_deg",
    })

    return df

if __name__ == '__main__':
    data = fetch_marine_data(latitude=40.19, longitude=-74.03)
    print(data.head())
    


