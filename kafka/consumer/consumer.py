from kafka import KafkaConsumer
from pymongo import MongoClient, errors as mongo_errors
import json
import os
import time
from datetime import datetime, timezone

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka1:9092,kafka2:9094,kafka3:9096")
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
            data["timestamp"] = datetime.now(timezone.utc)
            success = False

            for attempt in range (1, 5):
                try:               
                    collection.insert_one(data)
                    print(f"Data recieved and stored: {data}")
                    success = True
                    break
                except mongo_errors.PyMongoError as e:
                    print(f"Mongo insert failed (attempt {attempt}): {e}")
                    time.sleep(2)

            if success:
                consumer.commit_async()
            else:
                print(f"Message commit failed. Data: {data}")    

    except Exception as e:
        print(f"Error: {str(e)}")            

    finally:
        consumer.close()
        client.close()    

