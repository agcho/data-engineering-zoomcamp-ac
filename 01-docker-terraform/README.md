> pip install uv
> uv init --python 3.13
> uv run which python
> uv run python -V

> which python
> python -V 

> uv add pandas pyarrow

> uv add --dev jupyter
> uv run jupyter notebook

> docker run -it --entrypoint=bash --rm python:3.13
> pip --version

> docker-compose up

> Add pgadmin's port to PORTS

> Counting short trips

select count(*) as trips 
from green_taxi_2025_11
where lpep_pickup_datetime between '2025-11-01' and '2025-12-01'
and trip_distance <= 1;

> Longest trip for each day

select date(lpep_pickup_datetime) as pickup_day, 
	max(trip_distance) as max_trip_distance
from green_taxi_2025_11
where trip_distance < 100
group by pickup_day
order by max_trip_distance desc
limit 1;

> Biggest pickup zone

select gt."PULocationID", 
	sum(gt.total_amount) as total_revenue,
	tz."Zone"
from green_taxi_2025_11 gt
inner join taxi_zone_lookup tz
on gt."PULocationID" = tz."LocationID"
where DATE(gt.lpep_pickup_datetime) = '2025-11-18'
group by gt."PULocationID", tz."Zone"
order by total_revenue desc
limit 1;


> Largest tip

select gt."DOLocationID", 
	max(gt.tip_amount) as max_tip,
	tz."Zone"
from green_taxi_2025_11 gt
inner join taxi_zone_lookup tz
on gt."DOLocationID" = tz."LocationID"
where gt."PULocationID" = 74
group by gt."DOLocationID", tz."Zone"
order by max_tip desc
limit 1;