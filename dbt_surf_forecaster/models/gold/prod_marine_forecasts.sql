with base as (
    select 
        *
    from {{ref('stg_marine_forecasts')}}
)

select
    id
    , break_id
    , retrieved_at
    , forecast_time
    , extract(hour from forecast_time) as hour_of_day    
    , extract(month from forecast_time) as month    
    , wave_height_ft
    , swell_wave_height_ft
    , wind_wave_height_ft 
    , round(swell_wave_height_ft / nullif(wave_height_ft, 0), 2) as swell_ratio
    , swell_wave_period_s
    , swell_wave_direction_deg
    , case
        when swell_wave_direction_deg >= 348.75 or swell_wave_direction_deg < 11.25   then 'N'
        when swell_wave_direction_deg >= 11.25  and swell_wave_direction_deg < 33.75  then 'NNE'
        when swell_wave_direction_deg >= 33.75  and swell_wave_direction_deg < 56.25  then 'NE'
        when swell_wave_direction_deg >= 56.25  and swell_wave_direction_deg < 78.75  then 'ENE'
        when swell_wave_direction_deg >= 78.75  and swell_wave_direction_deg < 101.25 then 'E'
        when swell_wave_direction_deg >= 101.25 and swell_wave_direction_deg < 123.75 then 'ESE'
        when swell_wave_direction_deg >= 123.75 and swell_wave_direction_deg < 146.25 then 'SE'
        when swell_wave_direction_deg >= 146.25 and swell_wave_direction_deg < 168.75 then 'SSE'
        when swell_wave_direction_deg >= 168.75 and swell_wave_direction_deg < 191.25 then 'S'
        when swell_wave_direction_deg >= 191.25 and swell_wave_direction_deg < 213.75 then 'SSW'
        when swell_wave_direction_deg >= 213.75 and swell_wave_direction_deg < 236.25 then 'SW'
        when swell_wave_direction_deg >= 236.25 and swell_wave_direction_deg < 258.75 then 'WSW'
        when swell_wave_direction_deg >= 258.75 and swell_wave_direction_deg < 281.25 then 'W'
        when swell_wave_direction_deg >= 281.25 and swell_wave_direction_deg < 303.75 then 'WNW'
        when swell_wave_direction_deg >= 303.75 and swell_wave_direction_deg < 326.25 then 'NW'
        when swell_wave_direction_deg >= 326.25 and swell_wave_direction_deg < 348.75 then 'NNW'
    end as swell_wave_direction_cardinal      
    , round(sin(radians(swell_wave_direction_deg))::numeric, 4) as swell_wave_dir_sin
    , round(cos(radians(swell_wave_direction_deg))::numeric, 4) as swell_wave_dir_cos
    , wave_period_s
    , wave_direction_deg  
    , case
        when wave_direction_deg >= 348.75 or wave_direction_deg < 11.25   then 'N'
        when wave_direction_deg >= 11.25  and wave_direction_deg < 33.75  then 'NNE'
        when wave_direction_deg >= 33.75  and wave_direction_deg < 56.25  then 'NE'
        when wave_direction_deg >= 56.25  and wave_direction_deg < 78.75  then 'ENE'
        when wave_direction_deg >= 78.75  and wave_direction_deg < 101.25 then 'E'
        when wave_direction_deg >= 101.25 and wave_direction_deg < 123.75 then 'ESE'
        when wave_direction_deg >= 123.75 and wave_direction_deg < 146.25 then 'SE'
        when wave_direction_deg >= 146.25 and wave_direction_deg < 168.75 then 'SSE'
        when wave_direction_deg >= 168.75 and wave_direction_deg < 191.25 then 'S'
        when wave_direction_deg >= 191.25 and wave_direction_deg < 213.75 then 'SSW'
        when wave_direction_deg >= 213.75 and wave_direction_deg < 236.25 then 'SW'
        when wave_direction_deg >= 236.25 and wave_direction_deg < 258.75 then 'WSW'
        when wave_direction_deg >= 258.75 and wave_direction_deg < 281.25 then 'W'
        when wave_direction_deg >= 281.25 and wave_direction_deg < 303.75 then 'WNW'
        when wave_direction_deg >= 303.75 and wave_direction_deg < 326.25 then 'NW'
        when wave_direction_deg >= 326.25 and wave_direction_deg < 348.75 then 'NNW'
    end as wave_direction_cardinal      
    , round(sin(radians(wave_direction_deg))::numeric, 4) as wave_dir_sin
    , round(cos(radians(wave_direction_deg))::numeric, 4) as wave_dir_cos     

from base