from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import os
from datetime import datetime, timezone

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
TOPIC = os.getenv("KAFKA_TOPIC", "sensor-data")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "mongo-writer-group")

running = True

client = MongoClient(MONGO_URI)
db = client["sensor_db"]
collection = db["measurements"]

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers= KAFKA_BOOTSTRAP,
    auto_offset_reset = "earliest",
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    enable_auto_commit=False,
    group_id=GROUP_ID,
)

while running:
    try:
        for message in consumer:
            data = message.value
            data["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            collection.insert_one(data)
            print(f"Data recieved and stored: {data}")
            consumer.commit_async()

    except Exception as e:
        print(f"Error: {str(e)}")            

    finally:
        consumer.close()
        client.close()    

