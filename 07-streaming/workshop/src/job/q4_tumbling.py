from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment 

env = StreamExecutionEnvironment.get_execution_environment()
##env.get_configuration().set_string("pipeline.jars", "file:///path/to/flink-sql-connector-kafka-3.2.0.jar")
env.enable_checkpointing(10 * 1000)
env.set_parallelism(1)

settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = StreamTableEnvironment.create(env, environment_settings=settings)

# source (Kafka)
t_env.execute_sql("""
CREATE TABLE green_trips (
    lpep_pickup_datetime BIGINT,
    lpep_dropoff_datetime BIGINT,
    PULocationID INT,
    DOLocationID INT,
    passenger_count INT,
    trip_distance DOUBLE,
    tip_amount DOUBLE,
    total_amount DOUBLE,
    event_timestamp AS TO_TIMESTAMP_LTZ(lpep_pickup_datetime, 3),
    WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'green-trips',
    'properties.bootstrap.servers' = 'redpanda:29092',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json'
)
""")

# sink (Postgres)
t_env.execute_sql("""
CREATE TABLE trips_window_aggregated (
    window_start TIMESTAMP(3),
    PULocationID INT,
    num_trips BIGINT
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/postgres',
    'table-name' = 'trips_window_aggregated',
    'username' = 'postgres',
    'password' = 'postgres',
    'driver' = 'org.postgresql.Driver'
)
""")

# query
t_env.execute_sql("""
INSERT INTO trips_window_aggregated
SELECT
    TUMBLE_START(event_timestamp, INTERVAL '5' MINUTE),
    PULocationID,
    COUNT(*)
FROM green_trips
GROUP BY
    TUMBLE(event_timestamp, INTERVAL '5' MINUTE),
    PULocationID
""")