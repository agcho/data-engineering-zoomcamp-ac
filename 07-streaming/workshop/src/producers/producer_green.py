import dataclasses
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from kafka import KafkaProducer
from models import Ride, ride_from_row

TOPIC = "green-trips"
SERVER = "localhost:9092"
FILE = "../green_tripdata_2025-10.parquet"

COLUMNS = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "passenger_count",
    "trip_distance",
    "tip_amount",
    "total_amount"
]

def ride_serializer(ride):
    ride_dict = dataclasses.asdict(ride)
    json_str = json.dumps(ride_dict)
    return json_str.encode('utf-8')

def main():
    df = pd.read_parquet(FILE, columns=COLUMNS)

    producer = KafkaProducer(
        bootstrap_servers=[SERVER],
        value_serializer=ride_serializer
    )

    t0 = time.time()

    for _, row in df.iterrows():
    ##for row in df.to_dict(orient="records"):
        ride = ride_from_row(row)
        try:
            producer.send(TOPIC, value=ride).get(timeout=30)
        except Exception as e:
            print(f"Error sending message: {e}")

    try:
        producer.flush()
    except Exception as e:
        print(f"Error during flush: {e}")

    t1 = time.time()
    print(f'took {(t1 - t0):.2f} seconds')

if __name__ == "__main__":
    main()