from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

t_env = StreamTableEnvironment.create(env)

# source
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
CREATE TABLE tips_hourly (
    hour_start TIMESTAMP(3),
    total_tip DOUBLE
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/postgres',
    'table-name' = 'tips_hourly',
    'username' = 'postgres',
    'password' = 'postgres'
)
""")

# query
t_env.execute_sql("""
INSERT INTO tips_hourly
SELECT
    TUMBLE_START(event_timestamp, INTERVAL '1' HOUR),
    SUM(tip_amount)
FROM green_trips
GROUP BY
    TUMBLE(event_timestamp, INTERVAL '1' HOUR)
""")