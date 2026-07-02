with base as (
    select *
    from {{ ref('stg_weather_forecasts')}}
)

select
    id 
    , break_id 
    , retrieved_at
    , forecast_time
    , extract(hour from forecast_time) as hour_of_day    
    , extract(month from forecast_time) as month    
    , temperature_f
    , wind_speed_mph
    , wind_gusts_mph
    , wind_direction_deg
    , round(sin(radians(wind_direction_deg))::numeric, 4) as wind_dir_sin
    , round(cos(radians(wind_direction_deg))::numeric, 4) as wind_dir_cos   
    , case
        when wind_direction_deg >= 348.75 or wind_direction_deg < 11.25   then 'N'
        when wind_direction_deg >= 11.25  and wind_direction_deg < 33.75  then 'NNE'
        when wind_direction_deg >= 33.75  and wind_direction_deg < 56.25  then 'NE'
        when wind_direction_deg >= 56.25  and wind_direction_deg < 78.75  then 'ENE'
        when wind_direction_deg >= 78.75  and wind_direction_deg < 101.25 then 'E'
        when wind_direction_deg >= 101.25 and wind_direction_deg < 123.75 then 'ESE'
        when wind_direction_deg >= 123.75 and wind_direction_deg < 146.25 then 'SE'
        when wind_direction_deg >= 146.25 and wind_direction_deg < 168.75 then 'SSE'
        when wind_direction_deg >= 168.75 and wind_direction_deg < 191.25 then 'S'
        when wind_direction_deg >= 191.25 and wind_direction_deg < 213.75 then 'SSW'
        when wind_direction_deg >= 213.75 and wind_direction_deg < 236.25 then 'SW'
        when wind_direction_deg >= 236.25 and wind_direction_deg < 258.75 then 'WSW'
        when wind_direction_deg >= 258.75 and wind_direction_deg < 281.25 then 'W'
        when wind_direction_deg >= 281.25 and wind_direction_deg < 303.75 then 'WNW'
        when wind_direction_deg >= 303.75 and wind_direction_deg < 326.25 then 'NW'
        when wind_direction_deg >= 326.25 and wind_direction_deg < 348.75 then 'NNW'
    end as wind_direction_cardinal      

from base