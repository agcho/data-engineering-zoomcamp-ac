## Docker commands
> docker compose down -v
> docker compose build
> docker compose up -d

## Q1. Redpanda version
> docker exec -it workshop-redpanda-1 rpk version
> v25.3.9

## Q2. Sending data to Redpanda
> docker exec -it workshop-redpanda-1 rpk topic create green-trips --partitions 1 --replicas 1
> docker exec -it workshop-redpanda-1 rpk topic list
> docker exec -it workshop-redpanda-1 rpk topic consume green-trips
> docker exec -it workshop-redpanda-1 rpk topic consume green-trips -n 3
> python producer_green.py
> took 6.37 seconds  

## Q3. Consumser - trip distanct
> python consumer_green.py
> 8506  

## PyFlink

## Important notes for the Flink jobs:

> Place your job files in workshop/src/job/ - this directory is mounted into the Flink containers at /opt/src/job/
Submit jobs with: docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/your_job.py
> The green-trips topic has 1 partition, so set parallelism to 1 in your Flink jobs (env.set_parallelism(1)). With higher parallelism, idle consumer subtasks prevent the watermark from advancing.
> Flink streaming jobs run continuously. Let the job run for a minute or two until results appear in PostgreSQL, then query the results. You can cancel the job from the Flink UI at http://localhost:8081
> If you sent data to the topic multiple times, delete and recreate the topic to avoid duplicates: docker exec -it workshop-redpanda-1 rpk topic delete green-trips

## Q4. Tumbling window - pickup location
> docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/tumbling_window.py
> docker exec -it workshop-postgres-1 psql -U postgres
> docker exec -it workshop-postgres-1 psql -U postgres -d postgres
> CREATE DATABASE workshop;
> \l
> \dt
> \c workshop
> docker exec -it workshop-postgres-1 psql -U postgres -d workshop
> docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q4_tumbling.py
> docker compose exec jobmanager ./bin/flink run -py /opt/src/job/pass_through_job.py --pyFiles /opt/src -d
> 42

## Q5. Session window - longest streak
> docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q5_session.py
> SELECT MAX(num_trips) FROM trips_session;
> 52


## Q6. Tumbling window - largest tip 
> docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q6_tumbling.py
> SELECT hour_start FROM tips_hourly ORDER BY total_tip DESC LIMIT 1;
> 2025-10-16 18:00:00
