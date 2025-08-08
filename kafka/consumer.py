from kafka import KafkaConsumer
from pymongo import MongoClient
import json

running = True

client = MongoClient("mongodb://localhost:27017/")
db = client["sensor_db"]
collection = db["measurements"]

consumer = KafkaConsumer(
    "sensor-data",
    bootstrap_servers= "localhost:9092",
    auto_offset_reset = "earliest",
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    enable_auto_commit=False,
    group_id="mongo-writer-group",
)

while running:
    try:
        for message in consumer:
            data = message.value
            collection.insert_one(data)
            print(f"Data recieved and stored: {data}")
            consumer.commit_async()

    except Exception as e:
        print(f"Error: {str(e)}")            

    finally:
        consumer.close()
        client.close()    

