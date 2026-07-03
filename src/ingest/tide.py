import requests
import pandas as pd
import datetime

today = datetime.date.today()
start_date = today.strftime('%Y%m%d')

end_date = today + datetime.timedelta(days=7)
end_date = end_date.strftime('%Y%m%d')


def fetch_tide_data(
    station_id,
    url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    ):

    params = {
        "begin_date": start_date,
        "end_date": end_date,
        "station": station_id,
        "product": "predictions",
        "datum": "MLLW",
        "time_zone": "lst_ldt",
        "interval": "h",
        "units": "english",
        "application": "SurfForecastingPipeline",
        "format": "json",
    }

    responses = requests.get(url, params = params)
    responses.raise_for_status()
    data = responses.json()

    tide_data = pd.DataFrame(data['predictions'])

    return tide_data

def format_tides(df):
    df = df.copy()
    df = df.rename(columns = {
        't': 'time',
        'v': 'value',
    })

    return df

if __name__ == "__main__":
    data = fetch_tide_data(station_id="8531680")
    data = format_tides(data)
    print(data.head())
