import requests
import pandas as pd


def fetch_weather_data(
        latitude,  
        longitude, 
        hourly = ("temperature_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m"),
        timezone = "America/New_York", 
        forecast_days = 7, 
        url = "https://api.open-meteo.com/v1/forecast"
    ):
    """
    Pull data from marine API and extract hourly data
        - Temperature (in Celsius)
        - Windspeed (km/h)
        - Wind direction 
        - Wind gust speed (km/h)
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

    weather_data = pd.DataFrame(data['hourly'])

    return weather_data


def prepare_weather_data(df):
    '''
    Rename columns to prepare for ingestion into database
    '''
    df = df.copy()
    df = df.rename(columns={
    "time": "forecast_time",
    "temperature_2m": "temperature_c",
    "wind_speed_10m": "wind_speed_kmh",
    "wind_direction_10m": "wind_direction_deg",
    "wind_gusts_10m": "wind_gusts_kmh",
    })

    return df

if __name__ == '__main__':
    data = fetch_weather_data(latitude=40.19, longitude=-74.03)
    print(data.head())

