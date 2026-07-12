import pandas as pd
import numpy as np
import sys, os


sys.path.insert(0, os.path.abspath('.'))

from ingest.db import get_engine

def load_data():
    """
    Read final forecasts from database
    """
    df = pd.read_sql_table(table_name = 'fct_surf_forecasts', con = get_engine(), schema = 'gold')
    return df

def score_wind(wind_speed_mph, wind_dir_cardinal):
    """Score wind conditions out of 35 points."""
    offshore_dirs = {"W", "WNW", "WSW", "SW", "NW"}
    south_dirs = {"S", "SSW", "SSE"}
    north_dirs = {"N", "NNE", "NNW"}

    if wind_speed_mph < 3:
        return 30  # glassy, direction barely matters

    if wind_dir_cardinal in offshore_dirs:
        if wind_speed_mph < 20:
            return 35
        else:
            return 20  # too strong, still offshore though

    if wind_dir_cardinal in south_dirs:
        if wind_speed_mph < 12:
            return 25
        else:
            return 12

    if wind_dir_cardinal in north_dirs:
        return 8  # N winds suck, regardless of speed

    # onshore (E, ENE, ESE, SE)
    if wind_speed_mph < 8:
        return 18
    elif wind_speed_mph < 15:
        return 10
    else:
        return 3
    



def score_wave_quality(swell_wave_height_ft, swell_wave_period_s, swell_ratio, swell_direction):
    """Score wave quality out of 45 points."""
    good_directions = {'S', 'SSE', 'ESE'}
    bad_directions = {'E', 'ENE', 'NE'}

    # period tier - the primary driver of quality, independent of direction
    if swell_wave_period_s >= 13:
        period_score = 30
    elif swell_wave_period_s >= 10:
        period_score = 22
    elif swell_wave_period_s >= 7:
        period_score = 14
    else:
        period_score = 6

    # direction multiplier - rewards good swell direction, penalizes closeout prone ones
    if swell_direction in good_directions:
        direction_multiplier = 1.0
    elif swell_direction in bad_directions:
        direction_multiplier = 0.5
    else:
        direction_multiplier = 0.8  # neutral directions, mild penalty

    # height multiplier - very small swell caps quality regardless of period
    if swell_wave_height_ft < 1.5:
        height_multiplier = 0.5
    elif swell_wave_height_ft < 2.5:
        height_multiplier = 0.8
    else:
        height_multiplier = 1.0

    # swell ratio bonus - rewards clean conditions
    ratio_bonus = 15 * min(swell_ratio, 1.0)

    return round((period_score * direction_multiplier * height_multiplier) + ratio_bonus, 1)




def score_tide(tide_change_ft):
    """Score tide out of 20 points. Favors rising/mid tide."""
    if tide_change_ft is None:
        return 10  # neutral if missing

    if tide_change_ft > 0:
        return 20  # rising tide, generally favorable
    elif tide_change_ft == 0:
        return 12  # slack tide
    else:
        return 10  # falling tide, less ideal but not bad
    



def calculate_surf_score(row):
    """Combine wind, wave quality, and tide into a single 0-100 surfability score."""
    wind_pts = score_wind(row["wind_speed_mph"], row["wind_direction_cardinal"])
    wave_pts = score_wave_quality(
        row["swell_wave_height_ft"], 
        row["swell_wave_period_s"], 
        row["swell_ratio"],
        row["swell_wave_direction_cardinal"]
    )
    tide_pts = score_tide(row["tide_change_ft"])

    return round(wind_pts + wave_pts + tide_pts, 1)



def apply_scoring(df):
    scored_df = df.copy()
    scored_df['surf_score'] = df.apply(calculate_surf_score, axis = 1)

    return scored_df



if __name__ == "__main__":
    scored_forecasts = apply_scoring(load_data())
    print(scored_forecasts.head())
