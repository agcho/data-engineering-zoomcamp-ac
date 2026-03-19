import json
from time import time

from duckdb import df
import pandas as pd
from kafka import KafkaProducer

TOPIC = "green-trips"
SERVER = "localhost:9092"
FILE = "../../green_tripdata_2025-10.parquet"

COLUMNS = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "passenger_count",
    "trip_distance",
    "tip_amount",
    "total_amount",
]

def json_serializer(data):
    return json.dumps(data, ensure_ascii=False).encode("utf-8")

def main():
    df = pd.read_parquet(FILE)[COLUMNS].copy()

    df["lpep_pickup_datetime"] = int(pd.to_datetime(df["lpep_pickup_datetime"]).timestamp() * 1000)
    df["lpep_dropoff_datetime"] = int(pd.to_datetime(df["lpep_dropoff_datetime"]).timestamp() * 1000)

    producer = KafkaProducer(
        bootstrap_servers=[SERVER],
        value_serializer=json_serializer
    )

    t0 = time()

    for row in df.to_dict(orient="records"):
        producer.send(TOPIC, value=row)

    producer.flush()

    t1 = time()
    print(f"took {(t1 - t0):.2f} seconds")

if __name__ == "__main__":
    main()