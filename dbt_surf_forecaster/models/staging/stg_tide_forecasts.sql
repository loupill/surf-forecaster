with source as (
    select * from {{ source('raw', 'tide_forecasts') }}
)

select
    time as forecast_time
    , type as tide    
    , value as height
    , retrieved_at
from source