import json
from kafka import KafkaConsumer

TOPIC = "green-trips"
SERVER = "localhost:9092"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[SERVER],
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    consumer_timeout_ms=5000,
)

count = 0

for message in consumer:
    row = message.value
    dist = row.get("trip_distance")

    if dist is not None and float(dist) > 5.0:
        count += 1

print(count)