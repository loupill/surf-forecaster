with source as (
    select * from {{ source('raw', 'weather_forecasts') }}
)    

select
    id 
    , break_id 
    , retrieved_at
    , forecast_time

    -- Celsius to Farenheit
    , round(((temperature_c * 9.0/5.0) + 32)::numeric, 1) as temperature_f

    -- km/h to mph
    , round((wind_speed_kmh * 0.621371)::numeric, 1) as wind_speed_mph
    , round((wind_gusts_kmh * 0.621371)::numeric, 1) as wind_gusts_mph

    , wind_direction_deg
    
from source