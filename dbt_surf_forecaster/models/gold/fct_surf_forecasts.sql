with marine as (
    select *,
        row_number() over (
            partition by break_id, forecast_time 
            order by retrieved_at desc
        ) as rn
    from {{ ref('prod_marine_forecasts') }}
)

, weather as (
    select *,
        row_number() over (
            partition by break_id, forecast_time 
            order by retrieved_at desc
        ) as rn
    from {{ ref('prod_weather_forecasts') }}
)

, tide as (
    select *,
        row_number() over (
            partition by forecast_time 
            order by retrieved_at desc
        ) as rn
    from {{ ref('prod_tide_data') }}
)

, joined as (
    select
        marine.retrieved_at
        , marine.break_id
        , marine.forecast_time
        , marine.hour_of_day
        , marine.month

        -- marine features
        , marine.wave_height_ft
        , marine.swell_wave_height_ft
        , marine.wind_wave_height_ft
        , marine.swell_ratio
        , marine.swell_wave_period_s
        , marine.wave_period_s
        , marine.swell_wave_direction_deg
        , marine.swell_wave_dir_sin
        , marine.swell_wave_dir_cos
        , marine.swell_wave_direction_cardinal
        , marine.wave_direction_deg
        , marine.wave_dir_sin
        , marine.wave_dir_cos
        , marine.wave_direction_cardinal

        -- tide features
        , tide.tide
        , tide.height
        , tide.tide_change_ft

        -- weather features
        , weather.temperature_f
        , weather.wind_speed_mph
        , weather.wind_gusts_mph
        , weather.wind_direction_deg
        , weather.wind_dir_sin
        , weather.wind_dir_cos
        , weather.wind_direction_cardinal


    from marine
    inner join weather
        on  marine.break_id = weather.break_id
        and marine.forecast_time = weather.forecast_time
        and weather.rn = 1
        
    left join tide
       on marine.forecast_time = tide.forecast_time
       and tide.rn = 1
    where marine.rn = 1 
)

select * from joined