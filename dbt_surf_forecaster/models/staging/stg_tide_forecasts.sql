with source as (
    select * from {{ source('raw', 'tide_forecasts') }}
)

select
    cast(time as timestamptz) as forecast_time
    , type as tide    
    , cast(value as numeric) as height
    , retrieved_at
from source