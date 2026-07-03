with base as (
    select * from {{ref('stg_tide_forecasts')}}
)

select
    forecast_time
    , case
        when tide = 'L' then 'low'
        else 'high'
     end as tide   
    , height
    , (height - (lag(height) over (order by forecast_time))) as tide_change_ft
    , retrieved_at
from base