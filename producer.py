import pandas as pd
from kafka import KafkaProducer
import time
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"))

with open("synthetic_data.json", "r") as f:
    data = json.load(f)

topic_name = "sensor-data"

for entry in data:
    producer.send(topic_name, value= entry)    
    print(f"Data sent: {entry}")    
    time.sleep(1)

producer.flush()    