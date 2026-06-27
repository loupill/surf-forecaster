with source as (
    select * from {{ source('raw', 'marine_forecasts') }}
)

select
    id
    , break_id
    , retrieved_at
    , forecast_time

    -- convert meters to feet
    , round((wave_height_m * 3.281)::numeric, 2) as wave_height_ft
    , round((swell_wave_height_m * 3.281)::numeric, 2) as swell_wave_height_ft
    , round((wind_wave_height_m * 3.281)::numeric, 2) as wind_wave_height_ft
    
    , swell_wave_period_s
    , swell_wave_direction_deg
    , wave_period_s
    , wave_direction_deg
from source