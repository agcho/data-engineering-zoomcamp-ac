from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

t_env = StreamTableEnvironment.create(env)

# source
# (reuse same function)
def create_source_table(t_env):
    t_env.execute_sql("""
    CREATE TABLE green_trips (
        lpep_pickup_datetime STRING,
        lpep_dropoff_datetime STRING,
        PULocationID INT,
        DOLocationID INT,
        passenger_count INT,
        trip_distance DOUBLE,
        tip_amount DOUBLE,
        total_amount DOUBLE,

        event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
        WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'green-trips',
        'properties.bootstrap.servers' = 'redpanda:9092',
        'properties.group.id' = 'flink-group',
        'scan.startup.mode' = 'earliest-offset',
        'format' = 'json'
    )
    """)

create_source_table(t_env)

# sink
t_env.execute_sql("""
CREATE TABLE trips_session (
    PULocationID INT,
    session_start TIMESTAMP(3),
    num_trips BIGINT
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/postgres',
    'table-name' = 'trips_session',
    'username' = 'postgres',
    'password' = 'postgres'
)
""")

# query
t_env.execute_sql("""
INSERT INTO trips_session
SELECT
    PULocationID,
    SESSION_START(event_timestamp, INTERVAL '5' MINUTE),
    COUNT(*)
FROM green_trips
GROUP BY
    PULocationID,
    SESSION(event_timestamp, INTERVAL '5' MINUTE)
""")