from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

producer.send("green-trips", {"trip_distance": 7})
producer.flush()
print("Message sent!")