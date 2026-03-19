from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "green-trips",
    bootstrap_servers=["localhost:9092"],  # adjust if needed
    auto_offset_reset="earliest",
    consumer_timeout_ms=5000,  # stops after 5 seconds
    group_id="green-trips-test",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

count = 0
for msg in consumer:
    row = msg.value
    dist = row.get("trip_distance")
    print(row)  # debug: see all messages
    if dist is not None and float(dist) > 5.0:
        count += 1

print("Trips with distance > 5:", count)