-- Query to create dataset for lookalike days

-- Need to get the date of the human labelled session from labeling sessions table
-- Then need to associate if it was morning/midday/evening based on the time of day
-- Can then do the same for the scored forecasts and then join on that as a key (day + morning/midday/evening)


with associated_session as (
	select
		ls.session_date
		, hl.time_block
		, hl.rating
		, hl.comment
	from gold.human_labels hl 
	left join gold.labeling_sessions ls
		on hl.session_id = ls.id
) 

, time_group_logic as (
	select
		*
		, case when hour_of_day between 0 and 10 then 'morning'
			when hour_of_day between 11 and 15 then 'midday'
			when hour_of_day between 16 and 23 then 'evening'
			else null
		end as time_block
		, date(forecast_time) as forecast_date
	from gold.scored_forecasts
	
)

select
	tg.*
	, a.rating
	, a.comment
from time_group_logic tg
left join associated_session a
	on cast(forecast_date as date) = cast(a.session_date as date)
	and tg.time_block = a.time_block
where break_id = 'belmar'
order by forecast_time desc




